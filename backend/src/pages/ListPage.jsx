import { useEffect, useState } from "react";
import API from "../services/api";

const ListPage = () => {
const [data, setData] = useState([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
fetchData();
}, []);

const fetchData = async () => {
try {
const res = await API.get("/classified-data");
setData(res.data);
} catch (error) {
console.log("Error fetching data:", error);
} finally {
setLoading(false);
}
};

if (loading) {
return <h2 className="p-5">Loading data...</h2>;
}

if (!data || data.length === 0) {
return <h2 className="p-5">No records found</h2>;
}

return ( <div className="p-5"> <h1 className="text-xl font-bold mb-4">Data List</h1>

```
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
</div>


);
};

export default ListPage;

