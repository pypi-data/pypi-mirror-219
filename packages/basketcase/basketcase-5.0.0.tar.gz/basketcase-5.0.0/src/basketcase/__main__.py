import argparse
import sys

from . import basketcase


def main():
    """Handle command-line script execution."""

    parser = argparse.ArgumentParser(
        description='Download images and videos from Instagram.'
    )
    parser.add_argument(
        '-f',
        '--file',
        type=argparse.FileType('r'),
        help='A file containing a list of URLs separated by newline characters'
    )
    parser.add_argument(
        '-u',
        '--url',
        help='Download from a single URL'
    )
    parser.add_argument(
        '--cookie',
        help='Add a session cookie then exit'
    )
    parser.add_argument(
        '--cookie-name',
        help='''Provide a description for the new session cookie.
        Will be asked interactively if not specified.
        '''
    )
    parser.add_argument(
        '-l',
        '--list-sessions',
        help='List all available sessions then exit',
        action='store_true'
    )
    parser.add_argument(
        '--forget-session',
        help='Delete the specified session then exit',
        metavar='SESSION_ID',
        type=int
    )
    parser.add_argument(
        '-s',
        '--session',
        help='Use the specified session',
        metavar='SESSION_ID',
        type=int
    )
    parser.add_argument(
        '--set-default-session',
        help='Set the specified session as the default then exit',
        metavar='SESSION_ID',
        type=int
    )
    parser.add_argument(
        '--unset-default-session',
        help='Unset the default session then exit',
        action='store_true'
    )
    parser.add_argument(
        '--no-session',
        help="Don't use a session",
        action='store_true'
    )
    parser.add_argument(
        '--force',
        help='Ignore failed downloads',
        action='store_true',
        default=False
    )
    args = parser.parse_args()

    bc = basketcase.BasketCase(force_flag=args.force)

    if args.list_sessions:
        sessions = bc.authenticator.get_sessions()

        for session in sessions:
            print(f'{session["rowid"]!s}: {session["description"]}')

        return 0

    if args.set_default_session:
        bc.authenticator.set_default_session(args.set_default_session)
        print(f'Session marked as default: {args.set_default_session}')
        return 0

    if args.unset_default_session:
        bc.authenticator.unset_default_session()
        print(f'Default session mark removed')
        return 0

    if args.forget_session:
        bc.authenticator.forget_session(args.forget_session)
        print(f'Removed session id: {args.forget_session}')
        return 0

    if args.cookie:
        session = {
            'description': '',
            'cookie_id': args.cookie,
            'is_default': 0
        }

        if args.cookie_name:
            session['description'] = args.cookie_name
        else:
            session['description'] = input('Provide a short name to identify this cookie: ')

        session_id = bc.authenticator.new_session(session)
        print(f'Added session id: {session_id}')
        return 0

    if not args.no_session:
        if args.session:
            bc.authenticator.load_session(args.session)
        else:
            bc.authenticator.load_default()

    urls = set()

    if args.file:
        for line in args.file:
            line = line.rstrip()

            if line:
                urls.add(line)
    elif args.url:
        urls.add(args.url)
    else:
        raise RuntimeError('Use at least one of the arguments: --url, --input-file')

    bc.fetch(urls)
    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
