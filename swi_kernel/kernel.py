"""
Prolog Juypter kernel implementation for SWI-Prolog
"""


from .prolog_kernel import PrologBaseKernel
import requests
from bs4 import BeautifulSoup, Tag


class PrologKernel(PrologBaseKernel):
    kernel_name = 'swi_kernel'
    prolog_implementation_name = 'SWI-Prolog'
    additional_package_requirements = []
    implementation_version = '1.0'
    failure_response = 'false'
    success_response = 'true'
    error_prefix = 'ERROR: '
    informational_prefix = '% '
#    pl_path = '../prolog_server/jsonrpc_server.pl'
    pl_path = '../sicstus_swi_server/jsonrpc_server.pl'
    program_arguments = ['swipl', # default (looked up in $PATH)
                         '-l', pl_path,
                         '-t', 'jsonrpc_server_start',
                         '-q']

    kernel_display_name = prolog_implementation_name + ' kernel'
    implementation = kernel_display_name
    banner = kernel_display_name

# TODO inspection
