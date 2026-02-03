import { useEffect, useState } from "react";
import LeftBox from "./LeftBox"; 
import Sender from "./Sender";     // Add this import
import Receiver from "./Receiver";
import Text from "./Text";

function RightBoxInfo() {
    const [details, setDetails] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch("http://localhost:9797/userdata")
            .then(data => {
                if (!data.ok) {
                    throw new Error(`HTTP error! status: ${data.status}`);
                }
                return data.json();
            })
            .then(temp => {
                setDetails(temp);
                setLoading(false);
            })
            .catch(err => {
                console.error("Error fetching user data:", err);
                setError(err.message);
                setLoading(false);
            });
    }, []);
    
    if (loading) return <p>Loading cards...</p>;
    if (error) return <p>Error loading cards: {error}</p>;
    if (!details || details.length === 0) return <p>No cards found</p>;
    
    return (
        <>
            {details.map((values) => (
                <div key={values.id || values.name}>
                    <Sender sender={values.sender} />
                    <Receiver receiver={values.receiver} />
                    <Text/>
                </div>
            ))}
        </>
    );
}

export default RightBoxInfo;