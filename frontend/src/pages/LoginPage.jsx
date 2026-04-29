import { useState } from "react";
import { useAuth } from "../context/AuthContext";

const LoginPage = () => {
const { login } = useAuth();
const [form, setForm] = useState({ username: "", password: "" });

const handleSubmit = (e) => {
e.preventDefault();
const success = login(form.username, form.password);

```
if (!success) {
  alert("Invalid credentials");
}
```

};

return ( <div className="p-5"> <h2 className="text-xl font-bold mb-4">Login</h2>

```
  <form onSubmit={handleSubmit} className="space-y-3">
    <input
      placeholder="Username"
      onChange={(e) => setForm({ ...form, username: e.target.value })}
      className="border p-2 w-full"
    />
    <input
      type="password"
      placeholder="Password"
      onChange={(e) => setForm({ ...form, password: e.target.value })}
      className="border p-2 w-full"
    />

    <button className="bg-blue-500 text-white px-4 py-2">
      Login
    </button>
  </form>
</div>


);
};

export default LoginPage;
