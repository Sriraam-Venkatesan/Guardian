


function ProfilePage(props){
    
    return(
        <>
        <div className="navigation_bar" id="bar">
        <div id="title"><a href=""><h1 id="guardian">Guardian</h1></a></div>
        <div></div>
        <div id="options">
            <a href=""><h4>Connect with other Advocates</h4></a>
            <a href=""><h4>Select Victim</h4></a>
            <a href=""><h4>Chat</h4></a>
            <a href=""><h4>Logout</h4></a>
        </div>
    </div>
    <div className="main_page" id="page">
        <div id="desc">
            <img id="pfp" src={props.image} alt=""/>
            <div id="prof-desc"> <h1 id="name">{props.name}</h1>
            <p id="role">{props.role}</p>
           <p>Description: {props.description}</p>
            <p>Case Preferences: {props.case}</p>
        <button>Connect +</button>
        <button>Message</button>
            </div>
    </div>
    </div>
    <div className="helpline_bar" id="helpline">
        <h1 id="queries" >For Queries Contact</h1>
        <hr id="line1" />
        <p id="call">Phone Number: +91 7305896363</p>
        <p id="mail" >Mail Id:  sriraam1411@gmail.com</p>
    </div>
        </>
    );
}
export default ProfilePage