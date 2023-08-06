from __future__ import annotations

import typing

import toolcli
import toolstr
import toolsql

from ctc import cli
from ctc import config
from ctc import db
from ctc import spec


def get_command_spec() -> toolcli.CommandSpec:
    return {
        'f': status_command,
        'help': 'display database status',
        'args': [
            {
                'name': ['-v', '--verbose'],
                'help': 'display additional information',
                'action': 'store_true',
            },
        ],
        'examples': [''],
    }


def status_command(verbose: bool) -> None:
    styles = cli.get_cli_styles()

    toolstr.print_text_box('Database Status', style=styles['title'])
    print()
    context: spec.Context = {}
    db_config = config.get_context_db_config(
        context=context, schema_name='schema_versions'
    )
    if db_config is None:
        print('[no db configured]')
        return

    toolstr.print_header('Database Config', style=styles['title'])
    for key, value in db_config.items():
        if key == 'password':
            value = '********'
        cli.print_bullet(key=key, value=value)

    # print data being stored
    active_schemas = db.get_active_schemas()
    print()
    toolstr.print_header('Data to Store', style=styles['title'])
    networks = config.get_networks_that_have_providers()
    admin_schemas = db.get_admin_schema_names()
    generic_schemas = db.get_generic_schema_names()
    network_schemas = db.get_network_schema_names()
    toolstr.print('- admin schemas', style=styles['option'])
    for admin_schema in admin_schemas:
        toolstr.print('    -', admin_schema, style=styles['description'])
    toolstr.print('- generic schemas', style=styles['option'])
    for generic_schema in generic_schemas:
        toolstr.print('    -', generic_schema, style=styles['description'])
    toolstr.print('- evm schemas', style=styles['option'])
    for datatype in network_schemas:
        if active_schemas.get(datatype):
            toolstr.print('    -', datatype, style=styles['description'])
        else:
            toolstr.print(
                '    -', datatype, '(inactive)', style=styles['description']
            )
    toolstr.print('- networks', style=styles['option'])
    for network in networks:
        toolstr.print('    -', network, style=styles['description'])

    print()
    db_exists = toolsql.does_db_exist(db_config)
    if db_exists:

        with toolsql.connect(db_config) as conn:
            db_schema = toolsql.get_db_schema(conn)

        with toolsql.connect(db_config) as conn:
            if verbose:
                # toolsql.print_db_schema(db_schema=db_schema, styles=styles)

                print()
                toolstr.print_header('Schema Versions', style=styles['title'])
                rows = []
                for schema_name in active_schemas:
                    if schema_name in network_schemas:
                        schema_networks: typing.Sequence[
                            spec.NetworkReference
                        ] | typing.Sequence[
                            None
                        ] = config.get_networks_that_have_providers()
                    else:
                        schema_networks = [None]
                    for schema_network in schema_networks:
                        version = db.get_schema_version(
                            schema_name,
                            context=dict(network=schema_network),
                            conn=conn,
                        )
                        if version is None:
                            version = '[DNE]'

                        if schema_network is None:
                            network_str = ''
                        else:
                            network_str = str(schema_network)
                        row = [schema_name, network_str, version]
                        rows.append(row)
                    rows = sorted(rows, key=lambda row: tuple(row))
                toolstr.print_table(
                    rows,
                    labels=['schema', 'network', 'version'],
                    indent=4,
                    border=styles['comment'],
                    label_style=styles['title'],
                    column_styles={
                        'schema': styles['description'],
                        'network': 'bold',
                        'version': 'bold',
                    },
                )

                print()
                print()
                toolstr.print_header('Table Usage', style=styles['title'])
                toolsql.print_db_usage(conn, styles=styles)

    else:
        toolstr.print_text_box('Schema Summary', style=styles['title'])
        print('- db does not exist')

