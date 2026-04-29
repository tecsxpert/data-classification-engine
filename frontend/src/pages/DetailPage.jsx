import { useEffect, useState } from "react";
import API from "../services/api";

const DetailPage = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const res = await API.get("/classified-data/1"); // static id for now
      setData(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  if (!data) return <h2>Loading...</h2>;

  return (
    <div className="p-5">
      <h2 className="text-xl font-bold">Detail Page</h2>

      <p>File: {data.file_name}</p>
      <p>Type: {data.file_type}</p>
      <p>Label: {data.classification_label}</p>

      {/* SCORE BADGE */}
      <span className="bg-green-500 text-white px-2 py-1">
        Score: {data.confidence_score}
      </span>

      {/* ACTION BUTTONS */}
      <div className="mt-4 space-x-2">
        <button className="bg-blue-500 text-white px-3 py-1">
          Edit
        </button>

        <button className="bg-red-500 text-white px-3 py-1">
          Delete
        </button>
      </div>
    </div>
  );
};

export default DetailPage;
