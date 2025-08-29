import React, { useState, useEffect } from 'react';

const rolesList = [
  "Inside Sales", "B2B Sales", "Data Analytics", "Data Science",
  "Management Consulting", "Transition Consulting", "GCC Consulting",
  "Ecommerce", "Program Management", "Quality",
  "Finance Operations", "Sales Manager", "Digital Marketing", "Supply Chain"
];
const baatChitTopics = ["Self Doubt", "Peer Pressure", "Career Uncertainty", "Relationship"];
const timeSlots = ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"];

function generateMeetingLink() {
  return `https://zoom.us/j/${Math.floor(Math.random() * 1000000000)}`;
}

export default function App() {
  // User info + auth simulation with sign-in/sign-up mode
  const [user, setUser] = useState({ name: '', email: '', password: '', college:'', course:'', year:'' });
  const [loggedIn, setLoggedIn] = useState(false);
  const [loginMode, setLoginMode] = useState('signIn'); // 'signIn' or 'signUp'
  const [page, setPage] = useState('login');

  // Service selection & forms
  const [service, setService] = useState('');
  const [interviewPrepData, setInterviewPrepData] = useState({role:'', company:'', jd:'', sessionType:''});
  const [roleUnderstandingRole, setRoleUnderstandingRole] = useState('');
  const [baatChitSelectedTopics, setBaatChitSelectedTopics] = useState([]);

  // Scheduling
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedTime, setSelectedTime] = useState('');

  // Admin simulated data storage
  const [sessionRequests, setSessionRequests] = useState([]);

  // Session control
  const [currentSession, setCurrentSession] = useState(null);
  const [sessionTimer, setSessionTimer] = useState(0);
  const [sessionActive, setSessionActive] = useState(false);
  const [showPaymentPrompt, setShowPaymentPrompt] = useState(false);

  // Login form handler
  function handleLoginSubmit(e) {
    e.preventDefault();
    if(loginMode === 'signUp'){
      if(!user.name || !user.email || !user.password){
        alert('Please enter Name, Email and Password to sign up');
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
    setPage('serviceSelection');
  }

  // Toggle baat chit topics
  function toggleTopic(topic) {
    if (baatChitSelectedTopics.includes(topic)) {
      setBaatChitSelectedTopics(baatChitSelectedTopics.filter(t => t !== topic));
    } else {
      setBaatChitSelectedTopics([...baatChitSelectedTopics, topic]);
    }
  }

  // Submit session request
  function submitSessionRequest() {
    if(selectedDate === '' || selectedTime === ''){
      alert("Please select date and time");
      return;
    }
    if(service === ''){
      alert("Please select a service");
      return;
    }
    let sessionType = '';
    let role = '';
    let company = '';
    let jd = '';
    let topics = [];
    if(service === 'Interview Preparation'){
      if(interviewPrepData.sessionType === ''){
        alert("Please select a session type");
        return;
      }
      sessionType = interviewPrepData.sessionType;
      role = interviewPrepData.role;
      company = interviewPrepData.company;
      jd = interviewPrepData.jd;
      if(!role){
        alert('Please enter your role');
        return;
      }
    } else if(service === 'Role Understanding'){
      if(!roleUnderstandingRole){
        alert('Please select a role');
        return;
      }
      sessionType = 'Paid 60';
      role = roleUnderstandingRole;
    } else if(service === 'Baat Chit'){
      if(baatChitSelectedTopics.length === 0){
        alert('Please select at least one topic');
        return;
      }
      sessionType = 'Paid 60';
      topics = baatChitSelectedTopics;
    }
    const newRequest = {
      id: Date.now(),
      userEmail: user.email,
      userName: user.name || user.email,
      service,
      sessionType,
      role,
      company,
      jd,
      topics,
      date: selectedDate,
      time: selectedTime,
      adminStatus: 'Pending',
      meetingLink: '',
      paymentStatus: sessionType === 'Free 10' ? 'Pending' : 'Paid'
    };
    setSessionRequests([...sessionRequests, newRequest]);
    alert('Session request submitted for admin approval.');
    setPage('serviceSelection');
    resetForms();
  }

  function resetForms(){
    setInterviewPrepData({role:'', company:'', jd:'', sessionType:''});
    setRoleUnderstandingRole('');
    setBaatChitSelectedTopics([]);
    setSelectedDate('');
    setSelectedTime('');
  }

  // Admin panel actions
  function approveRequest(id){
    setSessionRequests(sessionRequests.map(r => {
      if(r.id === id){
        return {...r, adminStatus:'Accepted', meetingLink:generateMeetingLink()};
      }
      return r;
    }))
  }

  function declineRequest(id){
    setSessionRequests(sessionRequests.map(r => {
      if(r.id === id){
        return {...r, adminStatus:'Declined'};
      }
      return r;
    }))
  }

  // Admin Panel UI
  function renderAdminPanel(){
    return (
      <div style={{maxWidth: 600, margin: 'auto'}}>
        <h2>Admin Panel - Session Requests</h2>
        {sessionRequests.length === 0 && <p>No session requests.</p>}
        {sessionRequests.map(req => (
          <div key={req.id} style={{border: '1px solid #ccc', padding: 15, margin: 10, borderRadius: 8, backgroundColor:'#fffbe6'}}>
            <p><strong>{req.service} ({req.sessionType})</strong> for <em>{req.userName}</em> on <strong>{req.date}</strong> at <strong>{req.time}</strong></p>
            <p>Status: <strong>{req.adminStatus}</strong></p>
            {req.adminStatus === 'Accepted' && <p>Meeting link: <a href={req.meetingLink} target="_blank" rel="noreferrer">{req.meetingLink}</a></p>}
            {req.adminStatus === 'Pending' && <>
              <button onClick={() => approveRequest(req.id)} style={btnStyle}>Accept</button>
              <button onClick={() => declineRequest(req.id)} style={btnStyleDecline}>Decline</button>
            </>}
          </div>
        ))}
        <button onClick={() => setPage('serviceSelection')} style={btnStyleBack}>Back to Portal</button>
      </div>
    );
  }

  // Session Management
  useEffect(() => {
    if(sessionActive){
      const interval = setInterval(() => {
        setSessionTimer(t => t + 1);
      }, 60000);
      return () => clearInterval(interval);
    }
  }, [sessionActive]);

  useEffect(() => {
    if(!currentSession) return;
    if(currentSession.sessionType === 'Free 10' && sessionTimer >= 10){
      setSessionActive(false);
      setShowPaymentPrompt(true);
    }
    if(currentSession.sessionType === 'Paid 60' && sessionTimer >= 60){
      setSessionActive(false);
      alert('Session ended. Thank you!');
      setCurrentSession(null);
      setPage('serviceSelection');
    }
  }, [sessionTimer, currentSession]);

  function handlePaymentConfirm(){
    alert('Payment of INR 5999 received. Session extended by 50 mins.');
    setShowPaymentPrompt(false);
    setSessionActive(true);
    setSessionTimer(10);
  }

  function handlePaymentDecline(){
    alert('Session ended. Thank you!');
    setShowPaymentPrompt(false);
    setCurrentSession(null);
    setPage('serviceSelection');
  }

  const btnStyle = {
    backgroundColor: '#28a745',
    color: 'white',
    padding: '8px 16px',
    marginRight: 10,
    border: 'none',
    borderRadius: 5,
    cursor: 'pointer'
  };
  const btnStyleDecline = {...btnStyle, backgroundColor:'#dc3545'};
  const btnStyleBack = {...btnStyle, backgroundColor:'#007bff', marginTop: 20};
  const inputStyle = {
    width:'100%',
    padding:'8px',
    marginTop:'5px',
    borderRadius:'5px',
    border:'none',
    outline:'none',
    fontSize:'16px',
  };

  // Login/Register page
  if(!loggedIn && page === 'login'){
    return (
      <div style={{backgroundColor:'#007BFF', height:'100vh', display:'flex', justifyContent:'center', alignItems:'center'}}>
        <form onSubmit={handleLoginSubmit} style={{backgroundColor:'#FF6600', padding:30, borderRadius:10, boxShadow:'0 4px 10px rgba(0,0,0,0.3)', width:350, color:'white', display:'flex', flexDirection:'column', gap:20, fontFamily:"'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"}}>
          <h2 style={{margin:0, textAlign:'center'}}>{loginMode === 'signUp' ? 'Sign Up' : 'Sign In'}</h2>
          {loginMode === 'signUp' && <label>User Name
            <input type="text" value={user.name} onChange={e => setUser({...user, name:e.target.value})} required placeholder="Your name" style={inputStyle} />
          </label>}
          <label>Email ID
            <input type="email" value={user.email} onChange={e => setUser({...user,email:e.target.value})} required placeholder="example@mail.com" style={inputStyle} />
          </label>
          <label>Password
            <input type="password" value={user.password} onChange={e => setUser({...user,password:e.target.value})} required placeholder="Enter password" style={inputStyle} />
          </label>
          <button type="submit" style={{...btnStyleBack, backgroundColor:'#0056b3', cursor:'pointer'}}>{loginMode === 'signUp' ? 'Sign Up' : 'Sign In'}</button>
          <p style={{textAlign:'center', margin:0}}>
            {loginMode === 'signUp' ? 'Already have an account? ' : "Don't have an account? "}
            <span onClick={() => setLoginMode(loginMode === 'signUp' ? 'signIn' : 'signUp')} style={{cursor:'pointer', textDecoration:'underline'}}>
              {loginMode === 'signUp' ? 'Sign In' : 'Sign Up'}
            </span>
          </p>
        </form>
      </div>
    );
  }

  // Service Selection Page
  if(page === 'serviceSelection'){
    return (
      <div style={{maxWidth: 600, margin: 'auto', padding: 20}}>
        <h1>MBA Services Portal</h1>
        <div style={{display:'flex', justifyContent: 'space-around', marginBottom: 20}}>
          <button onClick={() => {setService('Interview Preparation'); setPage('interviewPrepForm')}} style={btnStyle}>Interview Preparation</button>
          <button onClick={() => {setService('Role Understanding'); setPage('roleUnderstandingForm')}} style={btnStyle}>Role Understanding</button>
          <button onClick={() => {setService('Baat Chit'); setPage('baatChitForm')}} style={btnStyle}>Baat Chit Session</button>
        </div>
        <button onClick={() => setPage('adminPanel')} style={{...btnStyle, backgroundColor:'#6c757d'}}>Admin Panel</button>
        <button onClick={() => {setLoggedIn(false); setPage('login');}} style={{...btnStyle, backgroundColor:'#dc3545', marginTop: 20}}>Logout</button>
      </div>
    );
  }

  // Interview Preparation form
  if(page === 'interviewPrepForm'){
    return (
      <div style={{maxWidth: 500, margin: 'auto', padding: 20}}>
        <h2>Interview Preparation</h2>
        <label>Role:
          <input type="text" value={interviewPrepData.role} onChange={e => setInterviewPrepData({...interviewPrepData, role: e.target.value})} style={inputStyle} />
        </label><br/>
        <label>Company:
          <input type="text" value={interviewPrepData.company} onChange={e => setInterviewPrepData({...interviewPrepData, company: e.target.value})} style={inputStyle} />
        </label><br/>
        <label>Job Description:
          <textarea value={interviewPrepData.jd} onChange={e => setInterviewPrepData({...interviewPrepData, jd: e.target.value})} style={{...inputStyle, height: 80}} />
        </label><br/>
        <label>Session Type:
          <select value={interviewPrepData.sessionType} onChange={e => setInterviewPrepData({...interviewPrepData, sessionType: e.target.value})} style={inputStyle}>
            <option value="">Select</option>
            <option value="Free 10">Free Session (10 mins)</option>
            <option value="Paid 60">Paid Session (60 mins) - INR 4999</option>
          </select>
        </label><br/>
        <div>
          <button onClick={() => setPage('scheduleSession')} style={btnStyle}>Next: Schedule Session</button>
          <button onClick={() => setPage('serviceSelection')} style={{...btnStyle, backgroundColor:'#6c757d', marginLeft: 10}}>Back</button>
        </div>
      </div>
    );
  }

  // Role Understanding form
  if(page === 'roleUnderstandingForm'){
    return (
      <div style={{maxWidth: 500, margin: 'auto', padding: 20}}>
        <h2>Role Understanding</h2>
        <label>Select Role:
          <select value={roleUnderstandingRole} onChange={e => setRoleUnderstandingRole(e.target.value)} style={inputStyle}>
            <option value="">Select</option>
            {rolesList.map(r => <option key={r} value={r}>{r}</option>)}
          </select>
        </label><br/>
        <p>Session cost: INR 499 (60 minutes)</p>
        <div>
          <button onClick={() => setPage('scheduleSession')} style={btnStyle}>Next: Schedule Session</button>
          <button onClick={() => setPage('serviceSelection')} style={{...btnStyle, backgroundColor:'#6c757d', marginLeft: 10}}>Back</button>
        </div>
      </div>
    );
  }

  // Baat Chit form
  if(page === 'baatChitForm'){
    return (
      <div style={{maxWidth: 500, margin: 'auto', padding: 20}}>
        <h2>Baat Chit Session</h2>
        <p>Select Topics:</p>
        {baatChitTopics.map(topic => (
          <label key={topic} style={{display:'block'}}>
            <input
              type="checkbox"
              checked={baatChitSelectedTopics.includes(topic)}
              onChange={() => toggleTopic(topic)}
            /> {topic}
          </label>
        ))}
        <p>Session cost: INR 499 (60 minutes)</p>
        <div>
          <button onClick={() => setPage('scheduleSession')} style={btnStyle}>Next: Schedule Session</button>
          <button onClick={() => setPage('serviceSelection')} style={{...btnStyle, backgroundColor:'#6c757d', marginLeft: 10}}>Back</button>
        </div>
      </div>
    );
  }

  // Schedule Session
  if(page === 'scheduleSession'){
    return (
      <div style={{maxWidth: 400, margin: 'auto', padding: 20}}>
        <h2>Schedule Session</h2>
        <label>Date: 
          <input 
            type="date" 
            min={new Date().toISOString().split('T')[0]} 
            value={selectedDate} 
            onChange={e => setSelectedDate(e.target.value)} 
            style={inputStyle} 
          />
        </label><br/>
        <label>Time Slot:
          <select value={selectedTime} onChange={e => setSelectedTime(e.target.value)} style={inputStyle}>
            <option value="">Select</option>
            {timeSlots.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </label><br/>
        <div>
          <button onClick={submitSessionRequest} style={btnStyle}>Submit Request</button>
          <button onClick={() => setPage('serviceSelection')} style={{...btnStyle, backgroundColor:'#6c757d', marginLeft: 10}}>Back</button>
        </div>
      </div>
    );
  }

  // Session running page
  if(page === 'session'){
    return (
      <div style={{maxWidth: 600, margin: 'auto', padding: 20}}>
        <h2>Current Session for {currentSession.userName}</h2>
        <p>Service: {currentSession.service}</p>
        <p>Session Type: {currentSession.sessionType}</p>
        <p>Time Elapsed: {sessionTimer} minutes</p>
        {sessionActive ? (
          <button 
            onClick={() => { 
              setSessionActive(false); 
              alert('Session ended. Thank you!'); 
              setPage('serviceSelection'); 
              setCurrentSession(null);
            }} 
            style={btnStyle}
          >
            End Session
          </button>
        ) : null}
        {showPaymentPrompt && (
          <div style={{border: '1px solid #ff4d4d', padding: 15, marginTop: 20, borderRadius: 5, backgroundColor: '#ffe6e6'}}>
            <p>Your free 10-min session has ended.</p>
            <p>Pay INR 5999 to continue for another 50 minutes.</p>
            <button onClick={handlePaymentConfirm} style={btnStyle}>Pay Now</button>
            <button onClick={handlePaymentDecline} style={{...btnStyleDecline, marginLeft: 10}}>End Session</button>
          </div>
        )}
      </div>
    )
  }

  return <div style={{padding: 20, textAlign:'center'}}>Loading...</div>;
}
