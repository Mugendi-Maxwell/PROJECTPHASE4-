import React from "react";

const Card = ({ title, description, children }) => {
  return (
    <div className="bg-white shadow-lg rounded-lg p-4 mb-4">
      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="text-gray-700">{description}</p>
      <div className="mt-4">{children}</div>
    </div>
  );
};

export default Card;
