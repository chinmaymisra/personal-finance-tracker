import React, { useState } from "react";
import axios from "axios";

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [success, setSuccess] = useState<boolean>(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
      setTransactions([]);
      setError("");
      setSuccess(false);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!file) {
      setError("Please select a file to upload.");
      setSuccess(false);
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      const response = await axios.post('http://localhost:8000/upload/', formData);
      setTransactions(response.data.transactions);
      setError("");
      setSuccess(true);
    } catch (error: any) {
      if (error.response && error.response.data && error.response.data.detail) {
        setError(error.response.data.detail);
      } else {
        setError("Failed to upload file. Please try again.");
      }
      setTransactions([]);
      setSuccess(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      padding: "40px",
      fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      backgroundColor: "#f2f2f2",
      minHeight: "100vh"
    }}>
      <div style={{
        backgroundColor: "#ffffff",
        padding: "30px",
        borderRadius: "10px",
        boxShadow: "0px 0px 10px rgba(0, 0, 0, 0.1)",
        maxWidth: "1200px",
        margin: "0 auto"
      }}>
        <h1 style={{ textAlign: "center", marginBottom: "20px" }}>Axis Bank Statement Parser</h1>

        <form onSubmit={handleSubmit} style={{ marginBottom: "20px", textAlign: "center" }}>
          <input
            type="file"
            onChange={handleFileChange}
            style={{
              marginBottom: "15px",
              display: "block",
              marginLeft: "auto",
              marginRight: "auto"
            }}
          />
          <button
            type="submit"
            style={{
              padding: "10px 20px",
              fontSize: "16px",
              cursor: "pointer",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "5px",
              transition: "background-color 0.3s"
            }}
            onMouseOver={e => (e.currentTarget.style.backgroundColor = "#0056b3")}
            onMouseOut={e => (e.currentTarget.style.backgroundColor = "#007bff")}
          >
            Upload
          </button>
        </form>

        {loading && <p style={{ textAlign: "center" }}>Processing your statement, please wait...</p>}

        {error && (
          <div style={{
            backgroundColor: "#ffcccc",
            padding: "10px",
            borderRadius: "5px",
            color: "#990000",
            marginBottom: "20px",
            textAlign: "center"
          }}>
            {error}
          </div>
        )}

        {success && (
          <div style={{
            backgroundColor: "#d4edda",
            padding: "10px",
            borderRadius: "5px",
            color: "#155724",
            marginBottom: "20px",
            textAlign: "center"
          }}>
            File uploaded successfully!
          </div>
        )}

        {!loading && transactions.length > 0 && (
          <>
            <h2 style={{ textAlign: "center" }}>Transactions</h2>
            <table style={{
              width: "100%",
              borderCollapse: "collapse",
              marginTop: "10px"
            }}>
              <thead>
                <tr>
                  <th style={thStyle}>Date</th>
                  <th style={thStyle}>Description</th>
                  <th style={thStyle}>Amount</th>
                  <th style={thStyle}>Transaction Type</th>
                  <th style={thStyle}>Balance</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((txn, idx) => (
                  <tr key={idx}>
                    <td style={tdStyle}>{txn.Date}</td>
                    <td style={tdStyle}>{txn.Description}</td>
                    <td style={tdStyle}>{txn.Amount}</td>
                    <td style={tdStyle}>{txn.TransactionType}</td>
                    <td style={tdStyle}>{txn.Balance}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}

        <footer style={{ marginTop: "30px", fontSize: "14px", color: "gray", textAlign: "center" }}>
          Only Axis Bank statements are supported currently.
        </footer>
      </div>
    </div>
  );
};

const thStyle = {
  border: "1px solid #ddd",
  padding: "8px",
  backgroundColor: "#007bff",
  color: "white",
  fontWeight: "bold" as const,
};

const tdStyle = {
  border: "1px solid #ddd",
  padding: "8px",
  textAlign: "center" as const,
};

export default UploadPage;
