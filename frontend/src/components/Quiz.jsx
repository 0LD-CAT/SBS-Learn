import { useState } from "react";

const Quiz = ({ block, langs }) => {
  const leftData = block[langs.left.slug];
  const rightData = block[langs.right.slug];

  const [selectedLeft, setSelectedLeft] = useState(null);
  const [selectedRight, setSelectedRight] = useState(null);

  if (!leftData || !rightData) return null;

  return (
    <div className="space-y-6">
      {/* LEFT LANGUAGE */}
      <div className="bg-gray-50 rounded-xl p-4">
        <h4 className="font-semibold mb-2 text-primary">
          {langs.left.name}
        </h4>

        <h3 className="text-lg font-semibold mb-3">
          {leftData.question}
        </h3>

        <div className="space-y-2">
          {leftData.answers.map((a, i) => (
            <button
              key={i}
              onClick={() => setSelectedLeft(i)}
              className={`w-full text-left p-3 rounded-lg border transition ${
                selectedLeft === i
                  ? a.correct
                    ? "bg-green-100 border-green-400"
                    : "bg-red-100 border-red-400"
                  : "hover:bg-gray-100"
              }`}
            >
              {a.text}
            </button>
          ))}
        </div>

        {selectedLeft !== null && (
          <p className="mt-3 text-sm text-gray-600">
            {leftData.explanation}
          </p>
        )}
      </div>

      {/* RIGHT LANGUAGE */}
      <div className="bg-gray-50 rounded-xl p-4">
        <h4 className="font-semibold mb-2 text-red-500">
          {langs.right.name}
        </h4>

        <h3 className="text-lg font-semibold mb-3">
          {rightData.question}
        </h3>

        <div className="space-y-2">
          {rightData.answers.map((a, i) => (
            <button
              key={i}
              onClick={() => setSelectedRight(i)}
              className={`w-full text-left p-3 rounded-lg border transition ${
                selectedRight === i
                  ? a.correct
                    ? "bg-green-100 border-green-400"
                    : "bg-red-100 border-red-400"
                  : "hover:bg-gray-100"
              }`}
            >
              {a.text}
            </button>
          ))}
        </div>

        {selectedRight !== null && (
          <p className="mt-3 text-sm text-gray-600">
            {rightData.explanation}
          </p>
        )}
      </div>
    </div>
  );
};

export default Quiz;