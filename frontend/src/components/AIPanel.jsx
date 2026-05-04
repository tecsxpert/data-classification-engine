import { useState } from "react";
import API from "../services/api";

const AIPanel = () => {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAI = async () => {
    setLoading(true);

    try {
      const res = await API.post("/ai/analyze", { text: input });
      setResponse(res.data.result);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-5 border mt-5">
      <h2 className="text-lg font-bold mb-2">AI Panel</h2>

      <textarea
        className="border w-full p-2"
        placeholder="Enter text..."
        onChange={(e) => setInput(e.target.value)}
      />

      <button
        onClick={handleAI}
        className="bg-blue-500 text-white px-4 py-2 mt-2"
      >
        Analyze
      </button>

      {/* Loading */}
      {loading && <p className="mt-2">Analyzing...</p>}

      {/* Response */}
      {response && (
        <div className="mt-3 p-3 border bg-gray-100">
          <h3 className="font-bold">Result</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default AIPanel;