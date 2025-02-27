from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)

# Database setup (SQLite in this case)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Donation model to store user data
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    blood_group = db.Column(db.String(10), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    medical_problem = db.Column(db.Text, nullable=True)
    terms_accepted = db.Column(db.Boolean, nullable=False)

    def _repr_(self):
        return f'<Donation {self.first_name} {self.last_name}>'

# Route to show the donation form
@app.route('/')
def index():
    return render_template('donation_form.html')  # Your HTML form file

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        first_name = request.form['first']
        last_name = request.form['last']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        gender = request.form['gender']
        blood_group = request.form['currentPos']
        state = request.form['state']
        city = request.form['city']
        area = request.form['area']
        pincode = request.form['pincode']
        medical_problem = request.form['problems']
        terms_accepted = 'prefer' in request.form

        # Create a new donation entry
        new_donation = Donation(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,  # Consider hashing this for security
            mobile=mobile,
            gender=gender,
            blood_group=blood_group,
            state=state,
            city=city,
            area=area,
            pincode=pincode,
            medical_problem=medical_problem,
            terms_accepted=terms_accepted
        )

        # Add to database and commit
        db.session.add(new_donation)
        db.session.commit()

        return redirect('/thank-you')  # Redirect to a thank you page

# Thank you page after successful submission
@app.route('/thank-you')
def thank_you():
    return "Thank you for your donation registration!"

if _name_ == '_main_':
    db.create_all()  # Creates the tables in the database
    app.run(debug=True)