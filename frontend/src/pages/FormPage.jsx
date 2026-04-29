import { useState } from "react";
import API from "../services/api";

const FormPage = () => {
  const [form, setForm] = useState({
    file_name: "",
    file_type: "",
    classification_label: "",
    confidence_score: ""
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const validate = () => {
    if (!form.file_name) return false;
    if (!form.classification_label) return false;
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validate()) {
      alert("Please fill required fields");
      return;
    }

    await API.post("/classified-data", form);
    alert("Data saved successfully");
  };

  return (
    <div className="p-5">
      <h2 className="text-xl font-bold">Create Data</h2>

      <form onSubmit={handleSubmit} className="space-y-3">
        <input name="file_name" placeholder="File Name" onChange={handleChange} className="border p-2 w-full" />
        <input name="file_type" placeholder="File Type" onChange={handleChange} className="border p-2 w-full" />
        <input name="classification_label" placeholder="Label" onChange={handleChange} className="border p-2 w-full" />
        <input name="confidence_score" placeholder="Confidence" onChange={handleChange} className="border p-2 w-full" />

        <button className="bg-blue-500 text-white px-4 py-2">
          Submit
        </button>
      </form>
    </div>
  );
};

export default FormPage;