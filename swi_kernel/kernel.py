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
    pl_path = '../prolog_server/jsonrpc_server.pl'
    program_arguments = ['swipl', # default (looked up in $PATH)
                         '-l', pl_path,
                         '-t', 'jsonrpc_server_start']

    kernel_display_name = prolog_implementation_name + ' kernel'
    implementation = kernel_display_name
    banner = kernel_display_name


    def do_inspect(self, code, cursor_pos, detail_level=0, omit_sections=()):
        """
        For SWI-Prolog, help for a predicate can be accessed with help/1.
        When inspecting a token, the output of this predicate precedes the docs for predicates from module jupyter.
        """
        # Get the matching predicates from module jupyter
        token, jupyter_data = self.get_token_and_jupyter_predicate_inspection_data(code, cursor_pos)

        if not token:
            # There is no token which can be inspected
            return {'status': 'ok', 'data': {}, 'metadata': {}, 'found': False}

        try:
            # Request predicate help with help/1
            response_dict = self.server_request(0, 'call', {'code':'help(' + token + ')'})
            help_output = response_dict["result"]["1"]["output"]

        except Exception as exception:
            self.logger.error(exception, exc_info=True)
            help_output = ''

        found = True

        if help_output == '':
            # There is no help/1 ouput
            if jupyter_data == {}:
                data = {}
                found = False
            else:
                data = jupyter_data
        else:
            # There is help/1 ouput
            jupyter_docs_plain = help_output
            jupyter_docs_md = '<pre>' + help_output.replace('\n', '<br>').replace('$', '&#36;') + '</pre>'

            if jupyter_data != {}:
                # Append the jupyter docs
                jupyter_docs_plain += '\n\n----------------------------------------------------------------------------\n\n' + jupyter_data['text/plain']
                jupyter_docs_md += '<br>----------------------------------------------------------------------------<br><br>' + jupyter_data['text/markdown']

            data = {'text/plain': jupyter_docs_plain, 'text/markdown': jupyter_docs_md}

        return {'status': 'ok', 'data': data, 'metadata': {}, 'found': found}
