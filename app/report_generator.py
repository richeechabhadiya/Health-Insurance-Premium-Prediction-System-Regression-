# from pathlib import Path
# from datetime import datetime

# def generate_html_report(inputs, premium, explanation=None, suggestions=None, out_path=None):
#     out_path = Path(out_path) if out_path else Path.cwd()/f'report_{int(datetime.now().timestamp())}.html'
#     html = ['<html><body>']
#     html.append(f'<h1>Insurance Premium Report</h1>')
#     html.append('<h2>User inputs</h2>')
#     html.append('<ul>')
#     for k,v in inputs.items():
#         html.append(f'<li><b>{k}</b>: {v}</li>')
#     html.append('</ul>')
#     html.append(f'<h2>Predicted premium: ₹{premium:.2f}</h2>')
#     if explanation:
#         html.append('<h3>Top contributors</h3><ul>')
#         for e in explanation:
#             html.append(f"<li>{e['feature']}: {e['shap']:.3f}</li>")
#         html.append('</ul>')
#     if suggestions:
#         html.append('<h3>Suggestions</h3><ul>')
#         for s in suggestions:
#             html.append(f'<li>{s}</li>')
#         html.append('</ul>')
#     html.append('</body></html>')
#     out_path.write_text('\n'.join(html), encoding='utf8')
#     return str(out_path)




def generate_report(inputs, premium, suggestions):
    text = f"""
INSURANCE REPORT
------------------------
Premium: ₹{premium:.2f}

Suggestions:
"""

    for s in suggestions:
        text += f"- {s}\n"

    return text