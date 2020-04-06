from django.contrib.auth.management.commands import createsuperuser as create_su
from main.models import UserProfile


class Command(create_su.Command):
    def handle(self, *args, **options):
        """
        Overridden method of createsuperuser's Command.
        Additionally creates a UserProfile for created User.
        """
        username = options[self.UserModel.USERNAME_FIELD]
        database = options['database']
        user_data = {}
        verbose_field_name = self.username_field.verbose_name
        try:
            self.UserModel._meta.get_field(create_su.PASSWORD_FIELD)
        except create_su.exceptions.FieldDoesNotExist:
            pass
        else:
            # If not provided, create the user with an unusable password.
            user_data[create_su.PASSWORD_FIELD] = None
        try:
            if options['interactive']:
                # Same as user_data but without many to many fields and with
                # foreign keys as fake model instances instead of raw IDs.
                fake_user_data = {}
                if hasattr(self.stdin, 'isatty') and not self.stdin.isatty():
                    raise create_su.NotRunningInTTYException
                default_username = create_su.get_default_username()
                if username:
                    error_msg = self._validate_username(username, verbose_field_name, database)
                    if error_msg:
                        self.stderr.write(error_msg)
                        username = None
                elif username == '':
                    raise create_su.CommandError('%s cannot be blank.' % create_su.capfirst(verbose_field_name))
                # Prompt for username.
                while username is None:
                    message = self._get_input_message(self.username_field, default_username)
                    username = self.get_input_data(self.username_field, message, default_username)
                    if username:
                        error_msg = self._validate_username(username, verbose_field_name, database)
                        if error_msg:
                            self.stderr.write(error_msg)
                            username = None
                            continue
                user_data[self.UserModel.USERNAME_FIELD] = username
                fake_user_data[self.UserModel.USERNAME_FIELD] = (
                    self.username_field.remote_field.model(username)
                    if self.username_field.remote_field else username
                )
                # Prompt for required fields.
                for field_name in self.UserModel.REQUIRED_FIELDS:
                    field = self.UserModel._meta.get_field(field_name)
                    user_data[field_name] = options[field_name]
                    while user_data[field_name] is None:
                        message = self._get_input_message(field)
                        input_value = self.get_input_data(field, message)
                        user_data[field_name] = input_value
                        if field.many_to_many and input_value:
                            if not input_value.strip():
                                user_data[field_name] = None
                                self.stderr.write('Error: This field cannot be blank.')
                                continue
                            user_data[field_name] = [pk.strip() for pk in input_value.split(',')]
                        if not field.many_to_many:
                            fake_user_data[field_name] = input_value

                        # Wrap any foreign keys in fake model instances
                        if field.many_to_one:
                            fake_user_data[field_name] = field.remote_field.model(input_value)

                # Prompt for a password if the model has one.
                while create_su.PASSWORD_FIELD in user_data and user_data[create_su.PASSWORD_FIELD] is None:
                    password = create_su.getpass.getpass()
                    password2 = create_su.getpass.getpass('Password (again): ')
                    if password != password2:
                        self.stderr.write("Error: Your passwords didn't match.")
                        # Don't validate passwords that don't match.
                        continue
                    if password.strip() == '':
                        self.stderr.write("Error: Blank passwords aren't allowed.")
                        # Don't validate blank passwords.
                        continue
                    try:
                        create_su.validate_password(password2, self.UserModel(**fake_user_data))
                    except create_su.exceptions.ValidationError as err:
                        self.stderr.write('\n'.join(err.messages))
                        response = input('Bypass password validation and create user anyway? [y/N]: ')
                        if response.lower() != 'y':
                            continue
                    user_data[create_su.PASSWORD_FIELD] = password
            else:
                # Non-interactive mode.
                # Use password from environment variable, if provided.
                if create_su.PASSWORD_FIELD in user_data and 'DJANGO_SUPERUSER_PASSWORD' in create_su.os.environ:
                    user_data[create_su.PASSWORD_FIELD] = create_su.os.environ['DJANGO_SUPERUSER_PASSWORD']
                # Use username from environment variable, if not provided in
                # options.
                if username is None:
                    username = create_su.os.environ.get('DJANGO_SUPERUSER_' + self.UserModel.USERNAME_FIELD.upper())
                if username is None:
                    raise create_su.CommandError('You must use --%s with --noinput.' % self.UserModel.USERNAME_FIELD)
                else:
                    error_msg = self._validate_username(username, verbose_field_name, database)
                    if error_msg:
                        raise create_su.CommandError(error_msg)

                user_data[self.UserModel.USERNAME_FIELD] = username
                for field_name in self.UserModel.REQUIRED_FIELDS:
                    env_var = 'DJANGO_SUPERUSER_' + field_name.upper()
                    value = options[field_name] or create_su.os.environ.get(env_var)
                    if not value:
                        raise create_su.CommandError('You must use --%s with --noinput.' % field_name)
                    field = self.UserModel._meta.get_field(field_name)
                    user_data[field_name] = field.clean(value, None)

            # Create User & UserProfile
            user = self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)
            user_profile = UserProfile(user=user)
            user_profile.save()

            if options['verbosity'] >= 1:
                self.stdout.write("Superuser created successfully.")
        except KeyboardInterrupt:
            self.stderr.write('\nOperation cancelled.')
            create_su.sys.exit(1)
        except create_su.exceptions.ValidationError as e:
            raise create_su.CommandError('; '.join(e.messages))
        except create_su.NotRunningInTTYException:
            self.stdout.write(
                'Superuser creation skipped due to not running in a TTY. '
                'You can run `manage.py createsuperuser` in your project '
                'to create one manually.'
            )
