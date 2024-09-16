from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container(
    [
        html.H1("Terms and Conditions", className='fade-in-text', style={'text-align': 'center', 'margin-top': '40px'}),
        html.P("Last updated: September 2024", className='fade-in-text', style={'text-align': 'center'}),
        
        html.H2("Introduction", className='fade-in-text', style={'margin-top': '40px'}),
        html.P("Welcome to TrendAnalyzer! These terms and conditions outline the rules and regulations for the use of our website and services, in compliance with applicable Spanish legislation.", className='fade-in-text'),
        
        html.H2("Intellectual Property Rights", className='fade-in-text', style={'margin-top': '40px'}),
        html.P("Other than the content you own, under these terms, TrendAnalyzer and/or its licensors own all the intellectual property rights and materials contained in this website, as recognized by Spanish intellectual property laws.", className='fade-in-text'),
        
        html.H2("Restrictions", className='fade-in-text', style={'margin-top': '40px'}),
        html.Ul(
            [
                html.Li("You are specifically restricted from publishing any website material in any other media without prior authorization.", className='fade-in-text'),
                html.Li("You are specifically restricted from selling, sublicensing, and/or otherwise commercializing any website material.", className='fade-in-text'),
                html.Li("You are specifically restricted from publicly performing and/or showing any website material.", className='fade-in-text'),
                html.Li("You are specifically restricted from using this website in any way that is or may be damaging to this website.", className='fade-in-text'),
                html.Li("You are specifically restricted from using this website in any way that impacts user access to this website.", className='fade-in-text'),
                html.Li("You are specifically restricted from using this website contrary to applicable Spanish laws and regulations, or in any way that may cause harm to the website, or to any person or business entity.", className='fade-in-text'),
                html.Li("You are specifically restricted from engaging in any data mining, data harvesting, data extracting, or any other similar activity in relation to this website.", className='fade-in-text'),
                html.Li("You are specifically restricted from using this website to engage in any advertising or marketing without written consent.", className='fade-in-text'),
            ]
        ),
        
        html.H2("Your Content", className='fade-in-text', style={'margin-top': '40px'}),
        html.P("In these terms and conditions, 'Your Content' shall mean any audio, video, text, images, or other material you choose to display on this website. By displaying Your Content, you grant TrendAnalyzer a non-exclusive, worldwide irrevocable, sub-licensable license to use, reproduce, adapt, publish, translate, and distribute it in any media, as per applicable Spanish law.", className='fade-in-text'),
        
        html.H2("No Warranties", className='fade-in-text', style={'margin-top': '40px'}),
        html.P("This website is provided 'as is,' with all faults, and TrendAnalyzer makes no representations or warranties of any kind related to this website or the materials contained on this website, in compliance with applicable consumer protection regulations in Spain.", className='fade-in-text'),
        
        html.H2("Limitation of Liability", className='fade-in-text', style={'margin-top': '40px'}),
        html.P("In no event shall TrendAnalyzer, nor any of its officers, directors, and employees, be held liable for anything arising out of or in any way connected with your use of this website, whether such liability is under contract or regulated by Spanish law. TrendAnalyzer, including its officers, directors, and employees, shall not be held liable for any indirect, consequential, or special liability arising out of or in any way related to your use of this website.", className='fade-in-text'),
        
        html.H2("Indemnification", className='fade-in-text', style={'margin-top': '40px'}),
        html.P("You hereby indemnify to the fullest extent TrendAnalyzer from and against any and/or all liabilities, costs, demands, causes of action, damages, and expenses arising in any way related to your breach of any of the provisions of these terms, in accordance with applicable Spanish law.", className='fade-in-text'),
        
        html.H2("Severability", className='fade-in-text', style={'margin-top': '40px'}),
        html.P("If any provision of these terms is found to be invalid under any applicable Spanish law, such provisions shall be deleted without affecting the remaining provisions herein.", className='fade-in-text'),
        
        html.H2("Variation of Terms", className='fade-in-text', style={'margin-top': '40px'}),
        html.P("TrendAnalyzer is permitted to revise these terms at any time as it sees fit, and by using this website, you are expected to review these terms on a regular basis in accordance with Spanish regulations.", className='fade-in-text'),
        
        html.H2("Assignment", className='fade-in-text', style={'margin-top': '40px'}),
        html.P("TrendAnalyzer is allowed to assign, transfer, and subcontract its rights and/or obligations under these terms without any notification, as per Spanish contractual law. However, you are not allowed to assign, transfer, or subcontract any of your rights and/or obligations under these terms.", className='fade-in-text'),
        
        html.H2("Entire Agreement", className='fade-in-text', style={'margin-top': '40px'}),
        html.P("These terms constitute the entire agreement between TrendAnalyzer and you in relation to your use of this website and supersede all prior agreements and understandings, subject to Spanish law.", className='fade-in-text'),
        
        html.H2("Governing Law & Jurisdiction", className='fade-in-text', style={'margin-top': '40px'}),
        html.P("These terms will be governed by and interpreted in accordance with the laws of Spain, and you submit to the exclusive jurisdiction of the courts located in Spain for the resolution of any disputes.", className='fade-in-text'),
    ],
    className='container-fluid',
)
