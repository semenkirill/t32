import { useNavigate, Link } from "react-router-dom";
import { useContext } from "react";
import AuthContext from "../context/AuthProvider";

const Home = () => {
    const { setAuth } = useContext(AuthContext);
    const navigate = useNavigate();

    const logout = async () => {
        // if used in more components, this should be in context 
        // axios to /logout endpoint 
        setAuth({});
        navigate('/');
    }

    return (
        <section>
            <h1>Home</h1>
            <br/>
            <p>You are logged in!</p>
            <br/>
            <Link to="/email">Go to the email page</Link>
            <br/>
            <br/>
            <Link to="/filelist">Go to the filelist</Link>
            <br/>
            <div className="flexGrow">
                <button onClick={logout}>Sign Out</button>
            </div>
        </section>
    )
}

export default Home
