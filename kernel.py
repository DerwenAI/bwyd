

from ipykernel.kernelbase import Kernel


class BwydKernel (Kernel):
    banner = "Bwyd kernel -- kitchen engineering"

    implementation_version = "0.1"
    implementation = "Bwyd"

    language_version = "0.1"
    language = "no-op"

    language_info = {
        "name": "Any text",
        "mimetype": "text/plain",
        "file_extension": ".bwyd",
    }


    def do_execute (
        self,
        code,
        silent,
        store_history = True,
        user_expressions = None,
        allow_stdin = False,
        ) -> dict:
        """
Simply echo any given input to `stdout`
        """
        if not silent:
            self.send_response(
                self.iopub_socket,
                "stream", 
                {
                    "name": "stdout",
                    "text": code,
                }
            )

        return {
            "status": "ok",
            "execution_count": self.execution_count, # base class increments execution count
            "payload": [],
            "user_expressions": {},
        }


if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class = BwydKernel)
