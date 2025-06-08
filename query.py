#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Prototype the use of KùzuDB
"""

import contextlib
import pathlib
import shutil
import sys

from icecream import ic
from pyinstrument import Profiler
from sentence_transformers import SentenceTransformer
import kuzu
import polars as pl


# sample data
TITLES = [
    "The Quantum World",
    "Chronicles of the Universe",
    "Learning Machines",
    "Echoes of the Past",
    "The Dragon's Call",
]

PUBLISHERS = [
    "Harvard University Press",
    "Independent Publisher",
    "Pearson",
    "McGraw-Hill Ryerson",
    "O'Reilly",
]

PUBLISHED_YEARS = [
    2004,
    2022,
    2019,
    2010,
    2015,
]


def db_connect (
    db_path: pathlib.Path = pathlib.Path("db"),
    ) -> kuzu.Connection:
    """
Initialize a KùzuDB connection, removing any previous data if it exits.
    """
    with contextlib.suppress(FileNotFoundError):
        shutil.rmtree(db_path)

    return kuzu.Connection(kuzu.Database(db_path))


def load_model (
    model_name: str = "all-MiniLM-L6-v2",
    ) -> SentenceTransformer:
    """
Load a pre-trained embedding generation model, defaulting to
<https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2>
for 384-dimensional embedding vectors.
    """
    return SentenceTransformer(model_name)


def main (
    ) -> int:
    """
Main entry point
    """
    profiler: Profiler = Profiler()
    model: SentenceTransformer = load_model()
    conn: kuzu.Connection = db_connect()

    ######################################################################
    ## set up schema

    # install and load vector extension
    # create tables
    conn.execute("INSTALL vector; LOAD vector;")
    conn.execute("CREATE NODE TABLE Book(id SERIAL PRIMARY KEY, title STRING, title_embedding FLOAT[384], published_year INT64);")
    conn.execute("CREATE NODE TABLE Publisher(name STRING PRIMARY KEY);")
    conn.execute("CREATE REL TABLE PublishedBy(FROM Book TO Publisher);")

    ## start code profiling
    profiler.start()

    # load dataframe
    df = pl.DataFrame([
        {
            "title": title,
            "publisher": publisher,
            "published_year": published_year,
        }
        for title, publisher, published_year in zip(TITLES, PUBLISHERS, PUBLISHED_YEARS)
    ])

    # insert sample data - Books with embeddings, Publishers
    # and create relationships between Books and Publishers
    for title, publisher, published_year in df.rows():
        title_embedding: list = model.encode(title).tolist()

        conn.execute(
            """CREATE (b:Book {title: $title, title_embedding: $title_embedding, published_year: $published_year});""",
            { "title": title, "title_embedding": title_embedding, "published_year": published_year, },
        )

        conn.execute(
            """CREATE (p:Publisher {name: $publisher});""",
            { "publisher": publisher, },
        )

        conn.execute(
            """
    MATCH (b:Book {title: $title})
    MATCH (p:Publisher {name: $publisher})
    CREATE (b)-[:PublishedBy]->(p);
            """,
            { "title": title, "publisher": publisher, },
        )

    ######################################################################
    ## vector search

    # vector search indexing
    conn.execute(
        """
    CALL CREATE_VECTOR_INDEX(
        'Book',
        'title_vec_index',
        'title_embedding'
    );
        """
    )

    # vector search query
    query: str = "quantum machine learning"
    query_vector: list = model.encode(query).tolist()

    result: QueryResult = conn.execute(
        """
    CALL QUERY_VECTOR_INDEX(
        'Book',
        'title_vec_index',
        $query_vector,
        2
    )
    RETURN node.title ORDER BY distance;
        """,
        { "query_vector": query_vector, },
    )

    ic(result.get_as_pl())

    result = conn.execute(
        """
    CALL QUERY_VECTOR_INDEX('book', 'title_vec_index', $query_vector, 2)
    WITH node AS n, distance
    MATCH (n)-[:PublishedBy]->(p:Publisher)
    RETURN p.name AS publisher, n.title AS book, distance
    ORDER BY distance LIMIT 5;
        """,
        { "query_vector": query_vector,},
    )

    ic(result.get_as_pl())

    ## end code profiling
    profiler.stop()
    profiler.print()


if __name__ == "__main__":
    main()
