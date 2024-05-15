from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


users = {}
current_user = None
all_meeting = []

@app.route('/', methods=['GET', 'POST'])
def login():
    global current_user
    
    if request.method == 'POST':
        email = request.form['username']  # Using email as the username
        password = request.form['password']
        print(users)
        # Check if email exists and password is correct
        if email in users and users[email]['password'] == password:
            current_user = users[email]  # Set the current user
           
            return redirect(url_for('meetings'))
        else:
            return "Invalid email or password"
    
    # If it's a GET request, render the login form
    return render_template('login.html')
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirmPassword']
        print(current_user)
        print(users)
        # Check if new password and confirm password match
        if new_password == confirm_password:
            # Update the password for the current user
            if current_user in users.values():
                for user in users:
                    if users[user] == current_user:
                        users[user]['password'] = new_password
                        return redirect(url_for('login'))
                return "User not found"
            else:
                return "User not found"
        else:
            return "Passwords do not match"
    else:
        return render_template('password.html')
@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    global current_user
    if request.method == 'POST':
        # Extract user information from the form submission
        name = request.form['name']
        student_id = request.form['studentid']
        date_of_birth = request.form['dateofbirth']
        email = request.form['email']
        password = request.form['password']
        
        # Store user information in the dictionary with email as key
        users[name] = {'email':email,'name': name, 'student_id': student_id, 'date_of_birth': date_of_birth, 'password': password}
        current_user = users[name]
        print(current_user)
        # Redirect to login page after sign up
        return redirect(url_for('login'))
    
    # If the request method is not POST, render the signup page
    return render_template('signup.html')


@app.route('/meeetings')
def meetings():
    return render_template('meetings.html', meetings=all_meeting)

@app.route('/add_new_meetings', methods=['GET','POST'])
def add_new_meetings():
    if request.method == 'POST':
        meeting_title = request.form['meetingTitle']
        tutor_name = request.form['tutorName']
        date = request.form['date']
        meeting_description = request.form['meetingDescription']
        
        new_meeting = {
            'title': meeting_title,
            'tutor': tutor_name,
            'date': date,
            'description': meeting_description
        }
        
        all_meeting.append(new_meeting)
        print(all_meeting)
        return redirect(url_for('meetings'))

    return render_template('add_new_meeting.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', current_user=current_user)

@app.route('/notification')
def notification():
    return render_template('notification.html', meetings=all_meeting)
@app.route('/tutor')
def tutor():
    print(all_meeting)
    return render_template('tutor.html', meetings=all_meeting)


if __name__ == '__main__':
    app.run(debug=True)
