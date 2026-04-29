import { useEffect, useState } from "react";
import API from "../services/api";

const ListPage = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);

  const fetchData = async () => {
    try {
      const res = await API.get(`/classified-data/all?page=${page}&size=5`);
      setData(res.data.content); // important for Spring Boot pagination
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setLoading(true);
    fetchData();
  }, [page]);

  // Loading state
  if (loading) {
    return <h2 className="p-5">Loading data...</h2>;
  }

  // Empty state
  if (data.length === 0) {
    return <h2 className="p-5">No records found</h2>;
  }

  return (
    <div className="p-5">
      <h1 className="text-xl font-bold mb-4">Data List</h1>

      <table className="border w-full">
        <thead>
          <tr>
            <th className="border p-2">File Name</th>
            <th className="border p-2">Type</th>
            <th className="border p-2">Label</th>
            <th className="border p-2">Confidence</th>
          </tr>
        </thead>

        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td className="border p-2">{item.file_name}</td>
              <td className="border p-2">{item.file_type}</td>
              <td className="border p-2">{item.classification_label}</td>
              <td className="border p-2">{item.confidence_score}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Pagination Buttons */}
      <div className="mt-4 space-x-2">
        <button
          onClick={() => setPage(page - 1)}
          disabled={page === 0}
          className="bg-gray-300 px-3 py-1"
        >
          Prev
        </button>

        <button
          onClick={() => setPage(page + 1)}
          className="bg-blue-500 text-white px-3 py-1"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default ListPage;