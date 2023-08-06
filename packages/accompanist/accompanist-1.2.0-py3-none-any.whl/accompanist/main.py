import click

from accompanist.cmd_hear import hear as hear_cmd
from accompanist.cmd_init import init as init_cmd
from accompanist.cmd_listen import listen as listen_cmd
from accompanist.cmd_play import play as play_cmd


@click.group(help="\
        \"Accompanist\" is your accompanist on AWS WAF log analyses.               \
        You can get an AWS WAF log analysis report by the following three commands.\
        (1) $ accompanist init    # Configure CWL log group setting              \
        (2) $ accompanist listen  # Get a WAF log file for analysis              \
        (3) $ accompanist play    # Analysis WAF logs and generate a report \
         \
        (Experimental) $ accompanist hear  # an alternative of listen for S3 \
        ")
@click.version_option()
def cmd() -> None:
    pass


cmd.add_command(init_cmd)
cmd.add_command(listen_cmd)
cmd.add_command(hear_cmd)
cmd.add_command(play_cmd)
