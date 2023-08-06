# Copyright (c) 2023 Matthias Mair<code@mjmair.com>
"""InvenHost integration plugin."""

import json
import logging

import requests
from django.conf.urls import url
# from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from plugin import InvenTreePlugin, registry
from plugin.mixins import EventMixin, SettingsMixin, UrlsMixin

logger = logging.getLogger('inventree')

LICENSE_ACCOUNT = 'd61ba105-f3f1-40ac-8bd8-55d741bebf21'
DEFAULT_HEADERS = {"Content-Type": "application/vnd.api+json", "Accept": "application/vnd.api+json"}


def superuser_check(user):
    """Check if a user is a superuser."""
    return user.is_superuser


def set_license_setting(setting):
    """Check licensing key setting."""
    if setting is not None and setting.value is not None:
        key = setting.value
        check_license_online(key, setting.plugin.set_metadata)


def check_license_online(key, set_fnc):
    """Check a licensing key online."""
    logger.info(f'Checking license key {key}')
    resp = requests.post(f'https://api.keygen.sh/v1/accounts/{LICENSE_ACCOUNT}/licenses/actions/validate-key', json={"meta": {"key": key}}, headers=DEFAULT_HEADERS)
    resp_data = resp.json()
    if (resp.status_code == 200 and resp_data['meta']['valid'] is True):
        logger.info(f"Licensing key {key} is valid")
        # Save the license key data
        set_fnc('inventree-core:license_valid', True)
        set_fnc('inventree-core:license_data', json.dumps(resp_data))
    else:
        logger.error(f"Licensing key {key} is invalid")
        set_fnc('inventree-core:license_valid', False)
        set_fnc('inventree-core:license_data', None)


def core_is_active():
    """Return if the core is active."""
    plg = registry.get_plugin('invenhost-core')
    if plg is None:
        return False
    if plg.get_setting('ACTIVE'):
        return plg.license_key_valid()
    return True


def ready():
    """Return if the core is ready."""
    return core_is_active()


class InvenHostCore(EventMixin, UrlsMixin, SettingsMixin, InvenTreePlugin):
    """InvenHost integration plugin."""

    NAME = 'InvenHostCore'
    SLUG = 'invenhost-core'
    TITLE = "InvenHost Core"
    MIN_VERSION = '0.12.0'

    SETTINGS = {
        'ACTIVE': {
            'name': _('Activate core'),
            'description': _('Activate the core integration - this is required for all other plugins'),
            'validator': bool,
            'default': False,
        },
        'LICENSE': {
            'name': _('License'),
            'description': _('License key for InvenHost'),
            'after_save': set_license_setting,
        },
    }

    def process_event(self, event, *args, **kwargs):
        """Process received events."""
        if event == 'plugins_loaded':
            check_license_online(self.get_setting('LICENSE'), self.db.set_metadata)

    def license_key_valid(self):
        """Return if the license key is valid."""
        return self.db.get_metadata('inventree-core:license_valid', False)

    def license_key_data(self):
        """Return the license key data."""
        data = self.db.get_metadata('inventree-core:license_data', None)
        if data is not None and data != {}:
            return json.loads(data)
        return None

    def view_check(self, request, pk=None, led=None, context=None):
        """Register an LED."""
        if not superuser_check(request.user):
            raise PermissionError("Only superusers can register an instance.")
        check_license_online(self.get_setting('LICENSE'), self.db.set_metadata)
        return redirect(self.settings_url)

    def setup_urls(self):
        """Return the URLs defined by this plugin."""
        return [
            url(r'check/', self.view_check, name='check'),
        ]

    def get_settings_content(self, request):
        """Add context to the settings panel."""
        valid = self.license_key_valid()
        data = self.license_key_data()

        key = data['data']['attributes']['key'] if (valid and data) else 'None'
        expires = data['data']['attributes']['expiry'] if (valid and data) else 'None'
        seats = data['data']['attributes']['maxMachines'] if (valid and data) else 'None'
        activations = data['data']['attributes']['uses'] if (valid and data) else 'None'
        last_check = data['data']['attributes']['lastValidated'] if (valid and data) else 'None'
        return f"""
        <h3>InvenTree core</h3>
        <p>Activate the core integration - this is required for all other plugins.</p>
        <p>With activating the plugin you accept that information about your instance is used for licensing services. When you activate the integration your plugins.txt gets appended with the custom packaging sources needed to install and update other InvenHost plugins.</p>
        <h5>License</h5>
        <button type="button" class="btn btn-primary" onclick="window.open('https://home.invenhost.com/license')">Get a license</button>
        <a class="btn btn-primary" href="{reverse('plugin:invenhost-core:check')}">Check license status</a>
        <table class="table table-bordered"><thead><tr><th>Key</th><th>Value</th></tr></thead><tbody>
        <tr><td>Valid</td><td>{valid}</td></tr>
        <tr><td>Key</td><td>{key}</td></tr>
        <tr><td>Expires</td><td>{expires}</td></tr>
        <tr><td>Seats</td><td>{seats}</td></tr>
        <tr><td>Activations</td><td>{activations}</td></tr>
        <tr><td>Last check</td><td>{last_check}</td></tr>
        </tbody></table>
        """
