import { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell
} from "recharts";

const AnalyticsPage = () => {

  const [period, setPeriod] = useState("weekly");

  const data = [
    { name: "Public", value: 8 },
    { name: "Confidential", value: 7 },
  ];

  const chartData = [
    { month: "Jan", files: 4 },
    { month: "Feb", files: 7 },
    { month: "Mar", files: 10 },
    { month: "Apr", files: 5 },
  ];

  return (
    <div className="p-5">

      <h1 className="text-2xl font-bold mb-5">
        Analytics Dashboard
      </h1>

      <div className="mb-5">
        <select
          value={period}
          onChange={(e) => setPeriod(e.target.value)}
          className="border p-2"
        >
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
          <option value="yearly">Yearly</option>
        </select>
      </div>

      <div className="mb-10">
        <BarChart width={500} height={300} data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="files" fill="#8884d8" />
        </BarChart>
      </div>

      <div>
        <PieChart width={400} height={300}>
          <Pie
            data={data}
            dataKey="value"
            outerRadius={100}
            label
          >
            <Cell fill="#0088FE" />
            <Cell fill="#FF8042" />
          </Pie>
          <Tooltip />
        </PieChart>
      </div>

    </div>
  );
};

export default AnalyticsPage;