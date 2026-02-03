import { useEffect, useState } from 'react';
import Profile from './profile';

function UserInfo() {
  const [details, setDetails] = useState([]);

  useEffect(() => {
    fetch('http://localhost:9292/userdata')
      .then(res => res.json())
      .then(data => setDetails(data))
      .catch(err => console.error(err));
  }, []);

  if (details.length === 0) return null;

  return (
    <>
      {details.map(info => (
        <Profile
          key={info.id}
          name={info.name}
          image={info.image}
          role={info.role}
          description={info.description}
          cost={info.cost}
        />
      ))}
    </>
  );
}

export default UserInfo;
