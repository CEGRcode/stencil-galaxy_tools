#!/usr/bin/env python
import argparse
import post_util_stencil

parser = argparse.ArgumentParser()
parser.add_argument('--config_file', dest='config_file', help='stats_config.ini')
parser.add_argument('--dbkey', dest='dbkey', help='Input dbkey')
parser.add_argument('--history_id', dest='history_id', help='History id')
parser.add_argument('--history_name', dest='history_name', help='History name')
parser.add_argument('--input', dest='input', help='Input dataset')
parser.add_argument('--input_datatype', dest='input_datatype', help='Input dataset datatype')
parser.add_argument('--input_post_type', dest='input_post_type', help='Input post type')
parser.add_argument('--input_id', dest='input_id', help='Encoded input dataset id')
parser.add_argument('--output', dest='output', help='Output dataset')
parser.add_argument('--stats_tool_id', dest='stats_tool_id', help='The caller of this script')
parser.add_argument('--tool_id', dest='tool_id', help='Tool that was executed to produce the input dataset')
parser.add_argument('--workflow_step_id', dest='workflow_step_id', default=None, help='Workflow step id')
parser.add_argument('--layout_id', dest='layoutId', default='sample layout', help='layout name for each section of Stencil website')
parser.add_argument('--tabId', dest='tabId', default='0', help='TabId, used to distnguish between elements in list')
parser.add_argument('--stepId', dest='stepId', default='0', help='stepId, used to distnguish between elements in each Tab')
parser.add_argument('--user_email', dest='user_email', help='Current user email')
args = parser.parse_args()

tool_parameters = ""
# Initialize the payload.
stderr = ''
payload = post_util_stencil.get_base_json_dict(args.config_file, args.dbkey, args.history_id, args.history_name, args.stats_tool_id, stderr, args.tool_id, tool_parameters, args.user_email, args.workflow_step_id)
# Generate the statistics and datasets.
payload['statistics'] = [{}]
payload['libraryData'] = [post_util_stencil.get_datasets(args.config_file, args.input_id, args.input_datatype, args.input_post_type, args.tool_id, args.workflow_step_id, args.layoutId, args.tabId, args.stepId)]  ## key changed from "datasets" to "libraryData" 
## also tool_id has been added as input to function
payload['history_url'] = post_util_stencil.get_history_url(args.config_file, args.history_id)
# Send the payload to PEGR.
stencil_url = post_util_stencil.get_stencil_url(args.config_file)
response = post_util_stencil.submit(args.config_file, payload)
# Make sure all is well.
post_util_stencil.check_response(stencil_url, payload, response)
# If all is well, store the results in the output.
post_util_stencil.store_results(args.output, stencil_url, payload, response)
