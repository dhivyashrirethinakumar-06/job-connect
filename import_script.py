import sqlite3
import pandas as pd

def import_job_seekers(excel_path):
    print(f"Reading file: {excel_path}")
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    conn = sqlite3.connect('job_portal.db')
    c = conn.cursor()
    
    col_map = {}
    for col in df.columns:
        cl = str(col).lower()
        if 'name' in cl: col_map['name'] = col
        elif 'mobile' in cl or 'contact' in cl or 'phone' in cl: col_map['mobile'] = col
        elif 'town' in cl or 'location' in cl or 'city' in cl: col_map['location'] = col
        elif 'skill' in cl or 'job' in cl or 'trade' in cl: col_map['skills'] = col
        elif 'age' in cl: col_map['experience'] = col

    if 'name' not in col_map or 'mobile' not in col_map:
        print("Error: Could not find 'Name' or 'Mobile' columns in the Excel file.")
        print(f"Columns found: {df.columns.tolist()}")
        return

    success_count = 0
    skip_duplicate = 0
    skip_invalid = 0
    new_users = []
    seen_mobiles = set()

    for _, row in df.iterrows():
        mobile_val = str(row[col_map['mobile']]).strip()
        if mobile_val.endswith('.0'):
            mobile_val = mobile_val[:-2]
        
        mobile_num = ''.join(filter(str.isdigit, mobile_val))
        
        if not mobile_num or len(mobile_num) < 10:
            skip_invalid += 1
            continue
            
        mobile_num = mobile_num[-10:]
        
        if mobile_num in seen_mobiles:
            skip_duplicate += 1
            continue
            
        c.execute("SELECT mobile FROM users WHERE mobile=?", (mobile_num,))
        if c.fetchone():
            skip_duplicate += 1
            seen_mobiles.add(mobile_num)
            continue
            
        name_val = str(row[col_map.get('name', '')]).strip()
        loc_val = str(row[col_map.get('location', '')]).strip() if 'location' in col_map else ''
        skills_val = str(row[col_map.get('skills', '')]).strip() if 'skills' in col_map else ''
        
        exp_raw = str(row[col_map.get('experience', '')]).strip()
        if exp_raw.endswith('.0'): exp_raw = exp_raw[:-2]
        exp_val = f"Age: {exp_raw}" if 'experience' in col_map else ''
        
        user_data = {
            'mobile': mobile_num,
            'role': 'Job Seeker',
            'name': name_val,
            'aadhar': '',
            'skills': skills_val,
            'experience': exp_val,
            'location': loc_val,
            'work_image': None,
            'password': '123'
        }
        
        new_users.append(user_data)
        seen_mobiles.add(mobile_num)

    if new_users:
        pd.DataFrame(new_users).to_sql('users', conn, if_exists='append', index=False)
        conn.commit()
    
    conn.close()
    
    print("-" * 30)
    print("IMPORT COMPLETE")
    print(f"Successfully inserted: {len(new_users)}")
    print(f"Skipped (Duplicates): {skip_duplicate}")
    print(f"Skipped (Invalid Number): {skip_invalid}")
    print("-" * 30)

if __name__ == "__main__":
    file_path = "job_seeker_details.xlsx"
    import_job_seekers(file_path)
