from swisseat import create_app
from swisseat.models import CmsSiteInfos

app = create_app()

@app.context_processor
def inject_globals():
    # Globale Variable bereitstellen
    mail_info = CmsSiteInfos.query.filter_by(variable='mail_info').first()
    mail_info = mail_info.content if mail_info else "Unbekannt"

    tel_support = CmsSiteInfos.query.filter_by(variable='tel_support').first()
    tel_support = tel_support.content if tel_support else "Unbekannt"

    company_info = CmsSiteInfos.query.filter_by(variable='company').first()
    company_name = company_info.content if company_info else 'Unbekannt'

    brand_info = CmsSiteInfos.query.filter_by(variable='brandname').first()
    brand_name = brand_info.content if brand_info else 'Unbekannt'

    address = CmsSiteInfos.query.filter_by(variable='address').first()
    address = address.content if address else 'Unbekannt'

    # Get Footer Content
    footer_info_title = CmsSiteInfos.query.filter_by(variable='footer_info_title').first()
    footer_info_title = footer_info_title.content if footer_info_title else "Unbekannt"

    footer_info_content = CmsSiteInfos.query.filter_by(variable='footer_info_content').first()
    footer_info_content = footer_info_content.content if footer_info_content else "Unbekannt"

    return dict(mail_info=mail_info,
                tel_support=tel_support,
                company_name=company_name,
                brand_name=brand_name,
                address=address,
                footer_info_title=footer_info_title,
                footer_info_content=footer_info_content)

if __name__ == '__main__':
    app.run(port=80, debug=True)
