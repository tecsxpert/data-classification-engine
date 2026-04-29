import { useAuth } from "../context/AuthContext";

const ProtectedRoute = ({ children }) => {
const { user } = useAuth();

if (!user) {
return <h2 className="p-5">Access Denied. Please login.</h2>;
}

return children;
};

export default ProtectedRoute;
