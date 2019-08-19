# Copyright (C) 2019 Magenta ApS, http://magenta.dk.
# Contact: info@magenta.dk.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import os
import logging
import requests

from django.template.loader import get_template
from django.core.mail import EmailMessage

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags

from constance import config

from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from service_person_stamdata_udvidet import get_citizen


logger = logging.getLogger(__name__)


def get_person_info(cpr):
    """
    Get CPR data on a person and his/her relations.
    """
    if settings.USE_SERVICEPLATFORM:
        func = get_cpr_data
    else:
        func = get_cpr_data_mock
    result = func(cpr)
    if not result:
        return None
    for relation in result["relationer"]:
        relation_cpr = relation["cprnr"]
        relation_data = func(relation_cpr)
        if relation_data:
            relation.update(relation_data)
    return result


def get_cpr_data(cpr):
    """
    Get CPR data from Serviceplatformen.
    """
    if not os.path.isfile(settings.SERVICEPLATFORM_CERTIFICATE_PATH):
        logger.info(
            "serviceplatform certificate path: %s is not a file",
            settings.SERVICEPLATFORM_CERTIFICATE_PATH,
        )
        return None
    try:
        result = get_citizen(
            service_uuids=settings.SERVICEPLATFORM_UUIDS,
            certificate=settings.SERVICEPLATFORM_CERTIFICATE_PATH,
            cprnr=cpr,
            production=settings.USE_SERVICEPLATFORM_PROD,
        )
        return result
    except requests.exceptions.HTTPError:
        logger.exception("get_cpr_data requests error")
        return None


def get_cpr_data_mock(cpr):
    """
    Use test data in place of the real 'get_cpr_data' for now.
    """
    result = {
        "statsborgerskab": "5100",
        "efternavn": "Jensen",
        "postdistrikt": "Næstved",
        "foedselsregistreringssted": "Myndighedsnavn for landekode: 5902",
        "boernUnder18": "false",
        "civilstandsdato": "1991-03-21+01:00",
        "adresseringsnavn": "Jens Jensner Jensen",
        "fornavn": "Jens Jensner",
        "tilflytningsdato": "2001-12-01+01:00",
        "markedsfoeringsbeskyttelse": "true",
        "vejkode": "1759",
        "standardadresse": "Sterkelsvej 17 A,2",
        "etage": "02",
        "koen": "M",
        "status": "80",
        "foedselsdato": "1978-04-27+01:00",
        "vejnavn": "Sterkelsvej",
        "statsborgerskabdato": "1991-09-23+02:00",
        "adressebeskyttelse": "false",
        "stilling": "Sygepl ske",
        "gaeldendePersonnummer": "2704785263",
        "vejadresseringsnavn": "Sterkelsvej",
        "civilstand": "G",
        "alder": "59",
        "relationer": [
            {"cprnr": "0123456780", "relation": "aegtefaelle"},
            {"cprnr": "1123456789", "relation": "barn"},
            {"cprnr": "2123456789", "relation": "barn"},
            {"cprnr": "3123456789", "relation": "barn"},
            {"cprnr": "0000000000", "relation": "mor"},
            {"cprnr": "0000000000", "relation": "far"},
        ],
        "postnummer": "4700",
        "husnummer": "017A",
        "vejviserbeskyttelse": "true",
        "kommunekode": "370",
    }
    return result


def send_activity_email(subject, template, activity):
    html_message = render_to_string(template, {"activity": activity})
    send_mail(
        subject,
        strip_tags(html_message),
        config.DEFAULT_FROM_EMAIL,
        [config.TO_EMAIL_FOR_PAYMENTS],
        html_message=html_message,
    )


def send_activity_created_email(activity):
    subject = _("Aktivitet oprettet")
    template = "emails/activity_created.html"
    send_activity_email(subject, template, activity)


def send_activity_updated_email(activity):
    subject = _("Aktivitet opdateret")
    template = "emails/activity_updated.html"
    send_activity_email(subject, template, activity)


def send_activity_expired_email(activity):
    subject = _("Aktivitet udgået")
    template = "emails/activity_expired.html"
    send_activity_email(subject, template, activity)


def send_appropriation(appropriation):
    """Generate PDF and XML files from appropriation and send them to SBSYS."""
    render_context = {"appropriation": appropriation}
    # Generate os2forms.xml
    xml_template = get_template(settings.SBSYS_XML_TEMPLATE)
    xml_data = xml_template.render(context=render_context)
    xml_file_name = "os2forms.xml"

    # Generate PDF
    html_template = get_template(settings.SBSYS_APPROPRIATION_TEMPLATE)
    html_data = html_template.render(context=render_context)

    # Configure fonts for correct rendering.
    font_config = FontConfiguration()
    pdf_data = HTML(string=html_data).write_pdf(font_config=font_config)
    pdf_file_name = f"{appropriation.sbsys_id}.pdf"

    # Send as email
    msg = EmailMessage()
    msg.subject = "SBSYS-journalisering"
    msg.body = ""
    msg.from_email = config.DEFAULT_FROM_EMAIL
    msg.to = [config.SBSYS_EMAIL]
    msg.attachments = [
        (xml_file_name, xml_data, "text/xml"),
        (pdf_file_name, pdf_data, "application/pdf"),
    ]

    msg.send()
