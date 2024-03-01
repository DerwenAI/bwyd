from ipykernel.kernelapp import IPKernelApp
from .kernel import BwydKernel

IPKernelApp.launch_instance(kernel_class = BwydKernel)
