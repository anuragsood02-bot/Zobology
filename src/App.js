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
  // Dummy meeting link generator
  return `https://zoom.us/j/${Math.floor(Math.random() * 1000000000)}`;
}

function App() {
  // User info + auth simulation
  const [user, setUser] = useState({email:'', password:'', name:'', college:'', course:'', year:''});
  const [loggedIn, setLoggedIn] = useState(false);

  // Navigation state
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

  // Login handler
  function handleLogin(e) {
    e.preventDefault();
    if(user.email && user.password && user.name) {
      setLoggedIn(true);
      setPage('serviceSelection');
    } else {
      alert('Please fill all login fields');
    }
  }

  // Handle toggling baat chit topics
  function toggleTopic(topic) {
    if (baatChitSelectedTopics.includes(topic)) {
      setBaatChitSelectedTopics(baatChitSelectedTopics.filter(t => t !== topic));
    } else {
      setBaatChitSelectedTopics([...baatChitSelectedTopics, topic]);
    }
  }

  // Submit session request form
  function submitSessionRequest() {
    // Basic validations
    if(selectedDate === '' || selectedTime === '') {
      alert("Please select date and time");
      return;
    }
    if(service === '') {
      alert("Please select a service");
      return;
    }
    let sessionType = '';
    let role = '';
    let company = '';
    let jd = '';
    let topics = [];
    if(service === 'Interview Preparation') {
      if(interviewPrepData.sessionType === '') {
        alert("Please select a session type");
        return;
      }
      sessionType = interviewPrepData.sessionType;
      role = interviewPrepData.role;
      company = interviewPrepData.company;
      jd = interviewPrepData.jd;
      if(!role) {
        alert('Please enter your role');
        return;
      }
    } else if(service === 'Role Understanding') {
      if(!roleUnderstandingRole) {
        alert('Please select a role');
        return;
      }
      sessionType = 'Paid 60';
      role = roleUnderstandingRole;
    } else if(service === 'Baat Chit') {
      if(baatChitSelectedTopics.length === 0) {
        alert('Please select at least one topic');
        return;
      }
      sessionType = 'Paid 60';
      topics = baatChitSelectedTopics;
    }
    // Create request object
    const newRequest = {
      id: Date.now(),
      userEmail: user.email,
      userName: user.name,
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

  // Reset form data
  function resetForms(){
    setInterviewPrepData({role:'', company:'', jd:'', sessionType:''});
    setRoleUnderstandingRole('');
    setBaatChitSelectedTopics([]);
    setSelectedDate('');
    setSelectedTime('');
  }

  // Admin simulation: List sessions and act
  function renderAdminPanel() {
    function approveRequest(id) {
      setSessionRequests(sessionRequests.map(r => {
        if(r.id === id) {
          return {...r, adminStatus: 'Accepted', meetingLink: generateMeetingLink()};
        }
        return r;
      }));
    }
    function declineRequest(id) {
      setSessionRequests(sessionRequests.map(r => {
        if(r.id === id) {
          return {...r, adminStatus: 'Declined'};
        }
        return r;
      }));
    }

    return (
      <div>
        <h2>Admin Panel - Session Requests</h2>
        {sessionRequests.length === 0 && <p>No session requests.</p>}
        {sessionRequests.map(req => (
          <div key={req.id} style={{border: '1px solid #aaa', padding: 10, margin: 10}}>
            <p><strong>{req.service} ({req.sessionType})</strong> for {req.userName} on {req.date} at {req.time}</p>
            <p>Status: {req.adminStatus}</p>
            {req.adminStatus === 'Accepted' && <p>Meeting link: <a href={req.meetingLink} target="_blank" rel="noreferrer">{req.meetingLink}</a></p>}
            {req.adminStatus === 'Pending' && (
              <>
                <button onClick={() => approveRequest(req.id)}>Accept</button>
                <button onClick={() => declineRequest(req.id)}>Decline</button>
              </>
            )}
          </div>
        ))}
        <button onClick={() => setPage('serviceSelection')}>Back to Portal</button>
      </div>
    )
  }

  // Simulate starting a session
  function startSessionForRequest(req) {
    setCurrentSession(req);
    setSessionTimer(0);
    setSessionActive(true);
    setShowPaymentPrompt(false);
    setPage('session');
  }

  // Session timer effect
  useEffect(() => {
    if(sessionActive) {
      const interval = setInterval(() => {
        setSessionTimer(t => t + 1);
      }, 60000); // 1 minute
      return () => clearInterval(interval);
    }
  }, [sessionActive]);

  // Session timeout handling
  useEffect(() => {
    if(!currentSession) return;
    if(currentSession.sessionType === 'Free 10' && sessionTimer >= 10) {
      setSessionActive(false);
      setShowPaymentPrompt(true);
    }
    if(currentSession.sessionType === 'Paid 60' && sessionTimer >= 60) {
      setSessionActive(false);
      alert('Session ended. Thank you!');
      setCurrentSession(null);
      setPage('serviceSelection');
    }
  }, [sessionTimer, currentSession]);

  // Payment prompt actions
  function handlePaymentConfirm() {
    alert('Payment of INR 5999 received. Session extended by 50 mins.');
    setShowPaymentPrompt(false);
    setSessionActive(true);
    setSessionTimer(10); // continue counting from 10 mins
  }
  function handlePaymentDecline() {
    alert('Session ended. Thank you!');
    setShowPaymentPrompt(false);
    setCurrentSession(null);
    setPage('serviceSelection');
  }

  // Main UI render
  if(!loggedIn){
    return (
      <div style={{maxWidth: 500, margin: 'auto'}}>
        <h1>MBA Services Portal - Login/Register</h1>
        <form onSubmit={handleLogin}>
          <input type="email" placeholder="Email" value={user.email} required 
            onChange={e => setUser({...user, email: e.target.value})} /><br/>
          <input type="password" placeholder="Password" value={user.password} required 
            onChange={e => setUser({...user, password: e.target.value})} /><br/>
          <input type="text" placeholder="Full Name" value={user.name} required 
            onChange={e => setUser({...user, name: e.target.value})} /><br/>
          <input type="text" placeholder="College" value={user.college} required 
            onChange={e => setUser({...user, college: e.target.value})} /><br/>
          <input type="text" placeholder="Course" value={user.course} required 
            onChange={e => setUser({...user, course: e.target.value})} /><br/>
          <input type="number" placeholder="Year" value={user.year} required min="1" max="5"
            onChange={e => setUser({...user, year: e.target.value})} /><br/>
          <button type="submit">Login / Register</button>
        </form>
      </div>
    );
  }

  if(page === 'serviceSelection'){
    return (
      <div style={{maxWidth: 600, margin: 'auto'}}>
        <h1>MBA Services Portal</h1>
        <button onClick={() => {setService('Interview Preparation'); setPage('interviewPrepForm')}}>Interview Preparation</button>
        <button onClick={() => {setService('Role Understanding'); setPage('roleUnderstandingForm')}}>Role Understanding</button>
        <button onClick={() => {setService('Baat Chit'); setPage('baatChitForm')}}>Baat Chit Session</button>
        <button onClick={() => setPage('adminPanel')}>Admin Panel</button>
        <button onClick={() => {setLoggedIn(false); setPage('login');}}>Logout</button>
      </div>
    );
  }

  if(page === 'interviewPrepForm'){
    return (
      <div style={{maxWidth: 500, margin: 'auto'}}>
        <h2>Interview Preparation</h2>
        <label>Role: <input type="text" value={interviewPrepData.role} onChange={e => setInterviewPrepData({...interviewPrepData, role: e.target.value})} /></label><br/>
        <label>Company: <input type="text" value={interviewPrepData.company} onChange={e => setInterviewPrepData({...interviewPrepData, company: e.target.value})} /></label><br/>
        <label>Job Description: <textarea value={interviewPrepData.jd} onChange={e => setInterviewPrepData({...interviewPrepData, jd: e.target.value})} /></label><br/>
        <label>Session Type:
          <select value={interviewPrepData.sessionType} onChange={e => setInterviewPrepData({...interviewPrepData, sessionType: e.target.value})}>
            <option value="">Select</option>
            <option value="Free 10">Free Session (10 mins)</option>
            <option value="Paid 60">Paid Session (60 mins) - INR 4999</option>
          </select>
        </label><br/>
        <button onClick={() => setPage('scheduleSession')}>Next: Schedule Session</button>
        <button onClick={() => setPage('serviceSelection')}>Back</button>
      </div>
    );
  }

  if(page === 'roleUnderstandingForm'){
    return (
      <div style={{maxWidth: 500, margin: 'auto'}}>
        <h2>Role Understanding</h2>
        <label>Select Role:
          <select value={roleUnderstandingRole} onChange={e => setRoleUnderstandingRole(e.target.value)}>
            <option value="">Select</option>
            {rolesList.map(r => <option key={r} value={r}>{r}</option>)}
          </select>
        </label><br/>
        <p>Session cost: INR 499 (60 minutes)</p>
        <button onClick={() => setPage('scheduleSession')}>Next: Schedule Session</button>
        <button onClick={() => setPage('serviceSelection')}>Back</button>
      </div>
    );
  }

  if(page === 'baatChitForm'){
    return (
      <div style={{maxWidth: 500, margin: 'auto'}}>
        <h2>Baat Chit Session</h2>
        <p>Select Topics:</p>
        {baatChitTopics.map(topic => (
          <label key={topic}>
            <input
              type="checkbox"
              checked={baatChitSelectedTopics.includes(topic)}
              onChange={() => toggleTopic(topic)}
            /> {topic}
          </label>
        ))}
        <p>Session cost: INR 499 (60 minutes)</p>
        <button onClick={() => setPage('scheduleSession')}>Next: Schedule Session</button>
        <button onClick={() => setPage('serviceSelection')}>Back</button>
      </div>
    );
  }

  if(page === 'scheduleSession'){
    return (
      <div style={{maxWidth: 400, margin: 'auto'}}>
        <h2>Schedule Session</h2>
        <label>Date: <input type="date" min={new Date().toISOString().split('T')[0]} value={selectedDate} onChange={e => setSelectedDate(e.target.value)} /></label><br/>
        <label>Time Slot:
          <select value={selectedTime} onChange={e => setSelectedTime(e.target.value)}>
            <option value="">Select</option>
            {timeSlots.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </label><br/>
        <button onClick={submitSessionRequest}>Submit Request</button>
        <button onClick={() => setPage('serviceSelection')}>Back</button>
      </div>
    );
  }

  if(page === 'adminPanel'){
    return renderAdminPanel();
  }

  if(page === 'session'){
    return (
      <div style={{maxWidth: 600, margin: 'auto'}}>
        <h2>Current Session for {currentSession.userName}</h2>
        <p>Service: {currentSession.service}</p>
        <p>Session Type: {currentSession.sessionType}</p>
        <p>Time Elapsed: {sessionTimer} minutes</p>
        {sessionActive ? (
          <button onClick={() => { setSessionActive(false); alert('Session ended. Thank you!'); setPage('serviceSelection'); setCurrentSession(null);}}>End Session</button>
        ) : null}
        {showPaymentPrompt && (
          <div style={{border: '1px solid red', padding: 15, marginTop: 20}}>
            <p>Your free 10-min session has ended.</p>
            <p>Pay INR 5999 to continue for another 50 minutes.</p>
            <button onClick={handlePaymentConfirm}>Pay Now</button>
            <button onClick={handlePaymentDecline}>End Session</button>
          </div>
        )}
      </div>
    )
  }

  return <div>Invalid state</div>;
}

export default App;
