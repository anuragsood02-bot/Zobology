import React, { useState, useEffect } from 'react';

const rolesList = [
  "Inside Sales", "B2B Sales", "Data Analytics", "Data Science",
  "Management Consulting", "Transition Consulting", "GCC Consulting",
  "Ecommerce", "Program Management", "Quality",
  "Finance Operations", "Sales Manager", "Digital Marketing", "Supply Chain",
  "Product Management"
];
const timeSlots = ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"];

function generateMeetingLink() {
  return `https://zoom.us/j/${Math.floor(Math.random() * 1000000000)}`;
}

export default function App() {
  const [user, setUser] = useState({ name: '', email: '', password: '', college:'', course:'' });
  const [loggedIn, setLoggedIn] = useState(false);
  const [loginMode, setLoginMode] = useState('signIn');
  const [page, setPage] = useState('login');

  const [service, setService] = useState('');
  const [interviewPrepData, setInterviewPrepData] = useState({ role:'', company:'', sessionType:'' });
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedTime, setSelectedTime] = useState('');
  const [sessionRequests, setSessionRequests] = useState([]);

  const btnStyle = {
    backgroundColor: '#FF6600',
    color: 'white',
    padding: '12px 20px',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: 16,
    margin: '5px'
  };
  const inputStyle = {
    width:'100%',
    padding:'8px',
    marginTop:'5px',
    marginBottom:'15px',
    borderRadius:'5px',
    border:'1px solid #ccc',
    fontSize:'16px',
  };
  const containerStyle = {
    maxWidth: 600,
    margin: 'auto',
    padding: '20px',
    backgroundColor: '#add8e6',
    minHeight:'100vh',
    boxSizing: 'border-box',
  };
  const boxStyle = {
    backgroundColor: '#FF6600',
    padding: '30px',
    borderRadius:'10px',
    boxShadow: '0 4px 10px rgba(0,0,0,0.3)',
    color:'white',
    width: '350px',
    margin: 'auto'
  };

  // Login / Sign up page
  if(!loggedIn && page === 'login'){
    return (
      <div style={{ backgroundColor: '#add8e6', height: '100vh', display: 'flex', flexDirection:'column', justifyContent: 'center', alignItems: 'center' }}>
        <h1 style={{color:'#003366', fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", marginBottom: '20px'}}>
          Zobology
        </h1>
        <div style={boxStyle}>
          <form onSubmit={e => {
            e.preventDefault();
            if(loginMode === 'signUp'){
              if(!user.email || !user.password || !user.name || !user.college || !user.course){
                alert('Please fill all sign up fields');
                return;
              }
              alert(`Signed Up as ${user.name}`);
            } else {
              if(!user.email || !user.password){
                alert('Please enter Email and Password to sign in');
                return;
              }
              alert(`Signed In as ${user.email}`);
            }
            setLoggedIn(true);
            setPage('home');
          }} style={{display:'flex', flexDirection:'column'}}>
            {loginMode === 'signUp' && <>
              <label>Name</label>
              <input 
                type="text" 
                value={user.name} 
                onChange={e => setUser({...user,name:e.target.value})} 
                placeholder="Your full name" 
                style={inputStyle} 
                required
              />
              <label>College</label>
              <input 
                type="text" 
                value={user.college} 
                onChange={e => setUser({...user,college:e.target.value})} 
                placeholder="College Name" 
                style={inputStyle} 
                required
              />
              <label>Course</label>
              <input 
                type="text" 
                value={user.course} 
                onChange={e => setUser({...user,course:e.target.value})} 
                placeholder="Course Name" 
                style={inputStyle} 
                required
              />
            </>}
            <label>Email ID</label>
            <input 
              type="email" 
              value={user.email} 
              onChange={e => setUser({...user,email:e.target.value})} 
              placeholder="example@mail.com" 
              style={inputStyle} 
              required
            />
            <label>Password</label>
            <input 
              type="password" 
              value={user.password} 
              onChange={e => setUser({...user,password:e.target.value})} 
              placeholder="Set your password" 
              style={inputStyle} 
              required
            />
            <button type="submit" style={btnStyle}>
              {loginMode === 'signUp' ? 'Sign Up' : 'Sign In'}
            </button>
          </form>
          <p style={{marginTop:'15px', textAlign:'center'}}>
            {loginMode === 'signUp' ? 'Already have an account? ' : "Don't have an account? "}
            <span 
              style={{textDecoration:'underline', cursor:'pointer'}}
              onClick={() => setLoginMode(loginMode === 'signUp' ? 'signIn' : 'signUp')}
            >
              {loginMode === 'signUp' ? 'Sign In' : 'Sign Up'}
            </span>
          </p>
        </div>
      </div>
    );
  }

  // Home Page
  if(page === 'home'){
    return (
      <div style={containerStyle}>
        <h1 style={{textAlign:'center', color:'#003366', fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"}}>
          Welcome to Zobology
        </h1>
        <p style={{whiteSpace:'pre-line', fontSize:18, textAlign:'center', marginTop:40, marginBottom:40}}>
{`We are not Bots, we are not using AI….we are humans, 10 years back we were students like you, seeking answers like 
interview me kya puchenge? Naukri milegi? Kaunsi industry achi hai? Kaunsa role acha hai? 

Obviously, we didn’t had much answers, I am sure you are also struggling with the same, that’s why we have created Zobology, to share our real world experiences.

We have your Jeetu Bhaiyas and Didis with us, from across the industries , different roles, who can help you prepare for your “Corporate Journey”`}
        </p>
        <div style={{display:'flex', justifyContent:'center'}}>
          <button style={btnStyle} onClick={() => {setService("Interview ki Tayaari"); setPage("interviewPrep")}}>
            Interview ki Tayaari
          </button>
          {/* Disabled buttons for future expansion */}
          <button style={{...btnStyle, opacity: 0.6, cursor: 'not-allowed'}} disabled>
            Role ki Jankaari
          </button>
          <button style={{...btnStyle, opacity: 0.6, cursor: 'not-allowed'}} disabled>
            Baat Chit Industry ke logo se
          </button>
        </div>
        <div style={{textAlign:'center', marginTop:'40px'}}>
          <button onClick={() => { setLoggedIn(false); setPage('login'); }} style={{ ...btnStyle, backgroundColor: '#dc3545' }}>Logout</button>
        </div>
      </div>
    );
  }

  // Interview Preparation Page
  if(page === 'interviewPrep'){
    return (
      <div style={containerStyle}>
        <div style={{maxWidth: 500, margin: 'auto'}}>
          <h2 style={{textAlign:'center', color:'#003366'}}>Interview ki Tayaari</h2>
          <label>Role</label>
          <select 
            value={interviewPrepData.role} 
            onChange={e => setInterviewPrepData({...interviewPrepData, role: e.target.value})} 
            style={inputStyle}
          >
            <option value="">Select Role</option>
            {rolesList.map(r => <option key={r} value={r}>{r}</option>)}
          </select>

          <label>Company Name</label>
          <input 
            type="text" 
            placeholder="Company Name" 
            value={interviewPrepData.company} 
            onChange={e => setInterviewPrepData({...interviewPrepData, company: e.target.value})} 
            style={inputStyle}
          />

          <label>Session Type</label>
          <select 
            value={interviewPrepData.sessionType} 
            onChange={e => setInterviewPrepData({...interviewPrepData, sessionType: e.target.value})} 
            style={inputStyle}
          >
            <option value="">Select Session Type</option>
            <option value="Free Session for 10 Mins">Free Session for 10 Mins</option>
            <option value="Paid Session for 60 mins">Paid Session for 60 mins - INR 4999</option>
          </select>

          <h3>Schedule Session</h3>
          <label>Date</label>
          <input 
            type="date" 
            min={new Date().toISOString().split('T')[0]} 
            value={selectedDate} 
            onChange={e => setSelectedDate(e.target.value)} 
            style={inputStyle} 
          />
          <label>Time Slot</label>
          <select 
            value={selectedTime} 
            onChange={e => setSelectedTime(e.target.value)} 
            style={inputStyle}
          >
            <option value="">Select Time Slot</option>
            {timeSlots.map(t => <option key={t} value={t}>{t}</option>)}
          </select>

          <div style={{marginTop:'20px', textAlign:'center'}}>
            <button style={btnStyle} onClick={() => {
              if(!interviewPrepData.role || !interviewPrepData.sessionType || !selectedDate || !selectedTime) {
                alert('Please fill all fields and schedule');
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
              setSessionRequests([...sessionRequests, newRequest]);
              alert('Interview Preparation session request submitted for admin approval.');
              setPage('home');
              setInterviewPrepData({role:'', company:'', sessionType:''});
              setSelectedDate('');
              setSelectedTime('');
            }}>Submit</button>
            <button style={{...btnStyle, backgroundColor:'#6c757d', marginLeft: 15}} onClick={() => setPage('home')}>Back</button>
          </div>
        </div>
      </div>
    );
  }

  return <div style={{padding: 20, textAlign: 'center', color:'#003366'}}>Page not implemented yet</div>;
}
