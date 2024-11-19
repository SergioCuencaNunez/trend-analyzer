from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container(
    [
        html.H1("Terms and Conditions", className='fade-in-text', style={'text-align': 'center', 'margin-top': '40px'}),
        html.P("Last updated: November 2024", className='fade-in-text', style={'text-align': 'center'}),
        
        html.H2("I. General Information", className='fade-in-text', style={'margin-top': '40px'}),
        html.P(
            "In compliance with Law 34/2002 on Services of the Information Society and Electronic Commerce (LSSI-CE), "
            "the following general information about this website is provided:",
            className='fade-in-text'
        ),
        html.Ul(
            [
                html.Li("Website Owner: Sergio Cuenca Núñez", className='fade-in-text'),
                html.Li("Address: Madrid, Spain", className='fade-in-text'),
                html.Li("Contact Email: scuenca06@gmail.com", className='fade-in-text'),
                html.Li("Domain Name: https://www.trendanalyzer.com", className='fade-in-text'),
            ]
        ),
        
        html.H2("II. Terms and General Conditions of Use", className='fade-in-text', style={'margin-top': '40px'}),
        html.H3("Purpose of the Website", className='fade-in-text'),
        html.P(
            "TrendAnalyzer is a platform for financial data analysis, interactive visualization, and predictive modeling. "
            "It is aimed at individual and corporate users seeking actionable insights into financial trends.",
            className='fade-in-text'
        ),
        html.H3("Modification and Access", className='fade-in-text'),
        html.P(
            "TrendAnalyzer reserves the right to modify, update, or remove any content on the website, as well as to "
            "temporarily or permanently interrupt access without prior notice. Access to the website is free of charge, "
            "except for connection costs incurred by the User.",
            className='fade-in-text'
        ),
        html.H3("User Condition", className='fade-in-text'),
        html.P(
            "The use, navigation, and access to the website imply the acceptance of these general conditions. Users agree "
            "to use the website and its services in accordance with applicable Spanish legislation and refrain from engaging "
            "in any activities that harm the website or other users.",
            className='fade-in-text'
        ),

        html.H2("III. Privacy Policy and Data Protection", className='fade-in-text', style={'margin-top': '40px'}),
        html.H3("Purpose of Data Processing", className='fade-in-text'),
        html.P(
            "The personal data provided by Users is processed solely to ensure proper operation, maintain the security of the "
            "platform, and inform Users about relevant updates and services.",
            className='fade-in-text'
        ),
        html.H3("Data Recipients", className='fade-in-text'),
        html.P(
            "TrendAnalyzer does not share personal data with third parties unless required by law or with explicit consent from "
            "the User. Robust security measures are in place in compliance with the General Data Protection Regulation (GDPR).",
            className='fade-in-text'
        ),
        html.H3("User Rights", className='fade-in-text'),
        html.P(
            "Users have the right to access, rectify, erase, and restrict the processing of their personal data. Requests can be "
            "made by contacting soporte@trendanalyzer.com.",
            className='fade-in-text'
        ),

        html.H2("IV. Exclusion of Warranties and Liability", className='fade-in-text', style={'margin-top': '40px'}),
        html.H3("Service Availability", className='fade-in-text'),
        html.P(
            "TrendAnalyzer does not guarantee uninterrupted availability or error-free operation of the website. The platform "
            "is provided 'as is' without warranties, as permitted by Spanish consumer protection laws.",
            className='fade-in-text'
        ),
        html.H3("Limitation of Liability", className='fade-in-text'),
        html.P(
            "TrendAnalyzer is not responsible for any financial decisions made based on the analysis provided by the platform "
            "or for damages caused by system failures, viruses, or unauthorized use of the platform.",
            className='fade-in-text'
        ),

        html.H2("V. Links Policy", className='fade-in-text', style={'margin-top': '40px'}),
        html.P(
            "The website may include links to third-party sites for informational purposes. TrendAnalyzer does not endorse or "
            "guarantee the content, accuracy, or availability of these external sites and will not be held liable for any damages "
            "arising from their use.",
            className='fade-in-text'
        ),

        html.H2("VI. Intellectual and Industrial Property", className='fade-in-text', style={'margin-top': '40px'}),
        html.P(
            "All intellectual and industrial property rights related to the content, design, and source code of this website "
            "belong to TrendAnalyzer, S.L. Reproduction, distribution, or public communication of any website content for "
            "commercial purposes is strictly prohibited without prior written authorization from TrendAnalyzer.",
            className='fade-in-text'
        ),

        html.H2("VII. Legal Actions, Applicable Law, and Jurisdiction", className='fade-in-text', style={'margin-top': '40px'}),
        html.H3("Legal Actions", className='fade-in-text'),
        html.P(
            "TrendAnalyzer reserves the right to take legal action, both civil and criminal, against unauthorized use of the "
            "website or its content that violates intellectual property or these terms.",
            className='fade-in-text'
        ),
        html.H3("Applicable Law and Jurisdiction", className='fade-in-text'),
        html.P(
            "The relationship between the User and TrendAnalyzer is governed by the laws of Spain. Any disputes arising from "
            "these terms will be resolved in the courts of Madrid, Spain.",
            className='fade-in-text'
        ),

        html.H2("VIII. Contact Information", className='fade-in-text', style={'margin-top': '40px'}),
        html.P(
            "For any inquiries or issues regarding these Terms and Conditions, please contact us via email at scuenca06@gmail.com "
            "or by phone at +34 606 558 403.",
            className='fade-in-text'
        ),
    ],
    className='container-fluid',
)
