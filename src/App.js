import React, { useState } from 'react';

// Inline SVG icon components defined before usage
const EmailIcon = () => (
  <svg width="20" height="20" fill="#343A40" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" style={{marginRight: 8}}>
    <path d="M1.998 6.993L12 13.195l10.002-6.202V18H1.998zM12 11L1.998 5h20.004L12 11z" />
  </svg>
);

const PasswordIcon = () => (
  <svg width="20" height="20" fill="#343A40" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" style={{marginRight: 8}}>
    <path d="M17 8H7v6h10V8zm-4 6a2 2 0 100-4 2 2 0 000 4z" />
    <path d="M5 8V6a7 7 0 1114 0v2h1a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2v-8a2 2 0 012-2h1zm2-2v2h10V6a5 5 0 00-10 0z" />
  </svg>
);

const colors = {
  blue: '#007BFF',
  white: '#FFFFFF',
  lightGray: '#F8F9FA',
  darkGray: '#343A40',
  teal: '#20C997',
  orange: '#FD7E14',
};

const rolesList = [
  "Inside Sales", "B2B Sales", "Data Analytics", "Data Science",
  "Management Consulting", "Transition Consulting", "GCC Consulting",
  "Ecommerce", "Program Management", "Quality",
  "Finance Operations", "Sales Manager", "Digital Marketing", "Supply Chain",
  "Product Management"
];

const timeSlots = ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"];

function App() {
  const [user, setUser] = useState({ name: '', email: '', password: '', college: '', course: '' });
  const [loggedIn, setLoggedIn] = useState(false);
  const [loginMode, setLoginMode] = useState('signIn');
  const [page, setPage] = useState('login');

  const [service, setService] = useState('');
  const [interviewPrepData, setInterviewPrepData] = useState({ role: '', company: '', sessionType: '' });
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedTime, setSelectedTime] = useState('');
  const [sessionRequests, setSessionRequests] = useState([]);

  const btnStyle = {
    backgroundColor: colors.orange,
    color: colors.white,
    padding: '12px 20px',
    border: 'none',
    borderRadius: 6,
    cursor: 'pointer',
    fontSize: 16,
    margin: 5,
  };

  const inputWrapper = {
    display: 'flex',
    alignItems: 'center',
    border: `1px solid ${colors.darkGray}`,
    borderRadius: 6,
    marginBottom: 20,
    padding: '8px 12px',
    backgroundColor: colors.white,
  };

  const input = {
    border: 'none',
    outline: 'none',
    fontSize: 16,
    flexGrow: 1,
  };

  const container = {
    fontFamily: `'Open Sans', 'Lato', Arial, sans-serif`,
    backgroundColor: colors.lightGray,
    minHeight: '100vh',
    padding: 0,
    margin: 0,
  };

  const formContainer = {
    maxWidth: 400,
    margin: '80px auto',
    backgroundColor: colors.white,
    borderRadius: 8,
    padding: 30,
    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
  };

  const header = {
    fontFamily: `'Montserrat', 'Poppins', sans-serif`,
    color: colors.blue,
    textAlign: 'center',
    fontSize: 32,
    marginBottom: 24,
    fontWeight: 700,
  };

  const navBar = {
    backgroundColor: colors.white,
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    padding: '0 24px',
    height: 60,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    fontFamily: `'Montserrat', 'Poppins', sans-serif`,
    color: colors.darkGray,
    fontWeight: 600,
  };

  const cardGrid = {
    display: 'flex',
    justifyContent: 'space-around',
    marginTop: 40,
  };

  const card = {
    backgroundColor: colors.white,
    borderRadius: 12,
    padding: 24,
    width: 200,
    boxShadow: '0 4px 10px rgba(0,0,0,0.07)',
    cursor: 'pointer',
    color: colors.darkGray,
    fontWeight: 700,
    fontSize: 18,
    textAlign: 'center',
    transition: 'box-shadow 0.3s',
  };

  const [hoveredCard, setHoveredCard] = useState(null);

  const WelcomeMessage = () => (
    <div style={{maxWidth: 700, margin: '40px auto', color: colors.darkGray, lineHeight: 1.6, fontSize: 18, fontWeight: 500, fontFamily: `'Open Sans', 'Lato', sans-serif`}}>
      <h2 style={{color: colors.orange, fontFamily: `'Montserrat', 'Poppins', sans-serif`, fontWeight: 700, textAlign: 'center', marginBottom: 24}}>Welcome to Zobology!</h2>
      <p>We’re not bots. We’re not powered by AI.</p>
      <p>We’re real people – with real stories – who once sat where you are now. Just a decade ago, we had questions like:</p>
      <p style={{color: colors.blue, fontWeight: 600, fontStyle: 'italic'}}>
        Interview mein kya puchenge?<br />
        Naukri milegi?<br />
        Kaunsi industry best hai?<br />
        Kaunsa role sahi hai?
      </p>
      <p>Back then, clear answers were hard to find. That’s why Zobology was created — to share honest, real-world experiences by people who’ve been in your shoes.</p>
      <p>Meet your Jeetu Bhaiyas and Didis — professionals from across industries and roles — ready to guide you on your corporate journey.</p>
      <h3 style={{color: colors.orange, marginTop: 30}}>Interview ki Tayaari</h3>
      <p>Connect with industry pros who've interviewed many candidates. Learn what interviewers seek, typical questions, how to tell your story, and how to lead your interview with the right words.</p>
      <h3 style={{color: colors.orange, marginTop: 24}}>Role ki Jaankari</h3>
      <p>Understand corporate roles by connecting with professionals. Learn about daily activities, challenges, growth opportunities, and what the job truly involves.</p>
      <h3 style={{color: colors.orange, marginTop: 24}}>Baat Chit</h3>
      <p>Talk about life, relationships, jobs, challenges, or ideas with young industry professionals who share the realities of corporate life and how to navigate them.</p>
    </div>
  );

  // Login Page JSX
  if (!loggedIn && page === 'login') {
    return (
      <div style={container}>
        <div style={formContainer}>
          <h1 style={header}>Zobology</h1>
          <form onSubmit={e => {
            e.preventDefault();
            if (loginMode === 'signUp') {
              if (!user.email || !user.password || !user.name || !user.college || !user.course) {
                alert('Please fill all sign up fields.');
                return;
              }
              alert(`Signed up as ${user.name}`);
            } else {
              if (!user.email || !user.password) {
                alert('Please enter Email and Password to sign in.');
                return;
              }
              alert(`Signed in as ${user.email}`);
            }
            setLoggedIn(true);
            setPage('home');
          }} noValidate>
            {loginMode === 'signUp' && <>
              <div style={inputWrapper}>
                <input
                  type="text"
                  placeholder="Name"
                  value={user.name}
                  onChange={e => setUser({ ...user, name: e.target.value })}
                  style={input}
                  required
                  aria-label="Name"
                />
              </div>
              <div style={inputWrapper}>
                <input
                  type="text"
                  placeholder="College"
                  value={user.college}
                  onChange={e => setUser({ ...user, college: e.target.value })}
                  style={input}
                  required
                  aria-label="College"
                />
              </div>
              <div style={inputWrapper}>
                <input
                  type="text"
                  placeholder="Course"
                  value={user.course}
                  onChange={e => setUser({ ...user, course: e.target.value })}
                  style={input}
                  required
                  aria-label="Course"
                />
              </div>
            </>}
            <div style={inputWrapper}>
              <EmailIcon />
              <input
                type="email"
                placeholder="Email ID"
                value={user.email}
                onChange={e => setUser({ ...user, email: e.target.value })}
                style={input}
                required
                aria-label="Email ID"
              />
            </div>
            <div style={inputWrapper}>
              <PasswordIcon />
              <input
                type="password"
                placeholder={loginMode === 'signUp' ? "Set Password" : "Password"}
                value={user.password}
                onChange={e => setUser({ ...user, password: e.target.value })}
                style={input}
                required
                aria-label="Password"
              />
            </div>
            <button type="submit" style={btnStyle}>
              {loginMode === 'signUp' ? 'Sign Up' : 'Sign In'}
            </button>
          </form>
          <p style={{ textAlign: 'center', marginTop: 14, color: colors.darkGray }}>
            {loginMode === 'signUp' ? 'Already have an account? ' : "Don't have an account? "}
            <span
              onClick={() => setLoginMode(loginMode === 'signUp' ? 'signIn' : 'signUp')}
              style={{ color: colors.blue, cursor: 'pointer', fontWeight: '600' }}
              role="button"
              tabIndex={0}
              onKeyPress={(e) => { if (e.key === 'Enter') setLoginMode(loginMode === 'signUp' ? 'signIn' : 'signUp'); }}
            >
              {loginMode === 'signUp' ? 'Sign In' : 'Sign Up'}
            </span>
          </p>
        </div>
      </div>
    );
  }

  // Home Page JSX
  if (page === 'home') {
    return (
      <div style={{ ...container, paddingTop: 60 }}>
        <nav style={navBar}>
          <div style={{ fontWeight: 700, fontSize: 24, color: colors.blue, fontFamily: `'Montserrat', 'Poppins', sans-serif` }}>Zobology</div>
          <div
            style={{ fontWeight: 600, color: colors.darkGray, cursor: 'pointer' }}
            onClick={() => {
              setLoggedIn(false);
              setPage('login');
            }}
            role="button" tabIndex={0}
            onKeyPress={(e) => { if (e.key === 'Enter') { setLoggedIn(false); setPage('login'); } }}
          >
            Logout
          </div>
        </nav>
        <main>
          <WelcomeMessage />
          <div style={cardGrid}>
            <div
              style={hoveredCard === 'interview' ? { ...card, boxShadow: '0 8px 16px rgba(0,0,0,0.15)' } : card}
              onMouseEnter={() => setHoveredCard('interview')}
              onMouseLeave={() => setHoveredCard(null)}
              onClick={() => { setService('Interview ki Tayaari'); setPage('interviewPrep'); }}
              role="button"
              tabIndex={0}
              onKeyPress={(e) => { if (e.key === 'Enter') { setService('Interview ki Tayaari'); setPage('interviewPrep'); } }}
            >
              Interview ki Tayaari
            </div>
            <div
              style={{ ...card, opacity: 0.5, cursor: 'not-allowed' }}
              title="Coming Soon"
            >
              Role ki Jankaari
            </div>
            <div
              style={{ ...card, opacity: 0.5, cursor: 'not-allowed' }}
              title="Coming Soon"
            >
              Baat Chit Industry ke logo se
            </div>
          </div>
        </main>
      </div>
    );
  }

  // Interview Preparation Booking Page
  if (page === 'interviewPrep') {
    return (
      <div style={container}>
        <nav style={navBar}>
          <div style={{ fontWeight: 700, fontSize: 24, color: colors.blue, fontFamily: `'Montserrat', 'Poppins', sans-serif` }}>Zobology</div>
          <div
            style={{ fontWeight: 600, color: colors.darkGray, cursor: 'pointer' }}
            onClick={() => setPage('home')}
            role="button"
            tabIndex={0}
            onKeyPress={(e) => { if (e.key === 'Enter') setPage('home'); }}
          >
            &#8592; Back
          </div>
        </nav>
        <main style={{ maxWidth: 600, margin: '40px auto', backgroundColor: colors.white, padding: 24, borderRadius: 10, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
          <h2 style={{ color: colors.orange, fontFamily: `'Montserrat', 'Poppins', sans-serif` }}>Interview ki Tayaari</h2>
          <label style={{ display: 'block', marginTop: 16, fontWeight: 600, color: colors.darkGray }}>Role:</label>
          <select
            value={interviewPrepData.role}
            onChange={e => setInterviewPrepData({ ...interviewPrepData, role: e.target.value })}
            style={{ ...input, marginBottom: 20 }}
            aria-label="Role selection"
          >
            <option value="">Select Role</option>
            {rolesList.map(r => <option key={r} value={r}>{r}</option>)}
          </select>

          <label style={{ display: 'block', marginBottom: 6, fontWeight: 600, color: colors.darkGray }}>Company Name:</label>
          <input
            type="text"
            placeholder="Company Name"
            value={interviewPrepData.company}
            onChange={e => setInterviewPrepData({ ...interviewPrepData, company: e.target.value })}
            style={input}
            aria-label="Company Name"
          />

          <label style={{ display: 'block', marginBottom: 6, fontWeight: 600, color: colors.darkGray }}>Session Type:</label>
          <select
            value={interviewPrepData.sessionType}
            onChange={e => setInterviewPrepData({ ...interviewPrepData, sessionType: e.target.value })}
            style={{ ...input, marginBottom: 20 }}
            aria-label="Session Type"
          >
            <option value="">Select Session Type</option>
            <option value="Free Session for 10 Mins">Free Session for 10 Mins</option>
            <option value="Paid Session for 60 mins">Paid Session for 60 mins - INR 4999</option>
          </select>

          <h3 style={{ color: colors.darkGray }}>Schedule Session</h3>
          <label>Date:</label>
          <input
            type="date"
            min={new Date().toISOString().split('T')[0]}
            value={selectedDate}
            onChange={e => setSelectedDate(e.target.value)}
            style={{ ...input, marginBottom: 15 }}
            aria-label="Session Date"
          />

          <label>Time Slot:</label>
          <select
            value={selectedTime}
            onChange={e => setSelectedTime(e.target.value)}
            style={{ ...input, marginBottom: 20 }}
            aria-label="Time Slot selection"
          >
            <option value="">Select Time Slot</option>
            {timeSlots.map(t => <option key={t} value={t}>{t}</option>)}
          </select>

          <div style={{ textAlign: 'center' }}>
            <button
              style={btnStyle}
              onClick={() => {
                if (!interviewPrepData.role || !interviewPrepData.sessionType || !selectedDate || !selectedTime) {
                  alert('Please fill all fields and schedule session.');
                  return;
                }
                const newRequest = {
                  id: Date.now(),
                  userEmail: user.email,
                  userName: user.name,
                  service: "Interview ki Tayaari",
                  sessionType: interviewPrepData.sessionType,
                  role: interviewPrepData.role,
                  company: interviewPrepData.company,
                  date: selectedDate,
                  time: selectedTime,
                  adminStatus: "Pending",
                  meetingLink: "",
                  paymentStatus: interviewPrepData.sessionType === 'Free Session for 10 Mins' ? 'Pending' : 'Paid'
                };
                alert('Session request submitted for admin approval.');
                setPage('home');
                setSelectedDate('');
                setSelectedTime('');
                setInterviewPrepData({ role: '', company: '', sessionType: '' });
                setSessionRequests([...sessionRequests, newRequest]);
              }}
            >
              Book Now
            </button>
          </div>
        </main>
      </div>
    );
  }

  return <div style={{padding: 20, textAlign: 'center', color: colors.darkGray}}>Loading...</div>;
}

