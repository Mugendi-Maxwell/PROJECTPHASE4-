import React from "react";

const InputField = ({ label, type = "text", value, onChange }) => {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-2">{label}</label>
      <input
        type={type}
        value={value}
        onChange={onChange}
        className="w-full p-2 border border-gray-300 rounded-md"
        required
      />
    </div>
  );
};

export default InputField;
