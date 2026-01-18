
import os

def parse_markdown_table_to_html(md_path, html_path):
    with open(md_path, 'r') as f:
        lines = f.readlines()

    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>French Vocabulary List</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 40px;
            color: #333;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
            border-top: 2px solid #333;
            border-bottom: 2px solid #333;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        /* Section headers within the table */
        .section-header {
            background-color: #e9ecef;
            font-weight: bold;
            text-align: center;
            color: #495057;
        }
        /* "Yes" in the Needed column */
        .needed-yes {
            color: #28a745;
            font-weight: 500;
        }
        /* "No" in the Needed column */
        .needed-no {
            color: #dc3545;
            font-weight: 500;
        }
        
        @media print {
            body { margin: 0; }
            table { box-shadow: none; }
            th { border-top: 1px solid #000; border-bottom: 1px solid #000; }
        }
    </style>
</head>
<body>

    <h1>French Exam Vocabulary</h1>

    <table>
        <thead>
            <tr>
                <th>French</th>
                <th>English</th>
                <th>Needed for Exam</th>
            </tr>
        </thead>
        <tbody>
"""

    # Skip the first two lines (Header row and dashes) as we manually added the header above
    # We will process the rest
    start_processing = False
    
    for line in lines:
        line = line.strip()
        if not line or not line.startswith('|'):
            continue
        
        # Check if it is the dash line
        if '---' in line:
            start_processing = True
            continue
            
        # If we haven't passed the dash line yet, ignore (unless we want to double check headers, but we hardcoded them)
        if not start_processing:
            continue

        # Split by pipe
        parts = [p.strip() for p in line.split('|')]
        # parts[0] is empty (before first pipe), parts[-1] is empty (after last pipe)
        # relevant data is parts[1], parts[2], parts[3]
        
        if len(parts) < 4:
            continue
            
        col1 = parts[1]
        col2 = parts[2]
        col3 = parts[3]

        # Check for section header
        # Logic: If col1 starts with ** and col2/col3 are empty
        if col1.startswith('**') and (not col2 or col2 == '') and (not col3 or col3 == ''):
            clean_header = col1.replace('**', '')
            html_content += f"""
            <tr>
                <td colspan="3" class="section-header">{clean_header}</td>
            </tr>
            """
        else:
            # Normal row
            needed_class = ""
            if col3.lower() == "yes":
                needed_class = "needed-yes"
            elif col3.lower() == "no":
                needed_class = "needed-no"
                
            html_content += f"""
            <tr>
                <td>{col1}</td>
                <td>{col2}</td>
                <td class="{needed_class}">{col3}</td>
            </tr>
            """

    html_content += """
        </tbody>
    </table>

</body>
</html>
"""

    with open(html_path, 'w') as f:
        f.write(html_content)
    
    print(f"Successfully converted {md_path} to {html_path}")

try:
    source = '/Users/admin/God-Line-1/God-Line-1/french_vocabulary.md'
    dest = '/Users/admin/God-Line-1/God-Line-1/french_vocabulary.html'
    parse_markdown_table_to_html(source, dest)
except Exception as e:
    print(f"Error: {e}")
