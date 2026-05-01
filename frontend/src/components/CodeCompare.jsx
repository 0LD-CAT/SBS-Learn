import Editor from "@monaco-editor/react";

const CodeCompare = ({ block }) => {
  const entries = Object.entries(block.snippets || {});

  return (
    <div className="bg-white rounded-2xl shadow p-6">
      {/* HEADER */}
      <h3 className="text-xl font-semibold mb-1">
        {block.title}
      </h3>

      {block.description && (
        <p className="text-gray-500 mb-5 text-sm md:text-base">
          {block.description}
        </p>
      )}

      {/* CODE GRID */}
      <div className="grid gap-4 md:grid-cols-2">
        {entries.map(([lang, snippet]) => (
          <div key={lang} className="min-w-0">
            {/* LANGUAGE LABEL */}
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">
                {snippet.label || lang}
              </span>
            </div>

            {/* MONACO WRAPPER */}
            <div className="border border-gray-200 rounded-xl overflow-hidden">
              <div className="h-[260px] md:h-[360px]">
                <Editor
                  width="100%"
                  height="100%"
                  //theme="vs-dark"
                  language={lang}
                  value={snippet.code}
                  options={{
                    readOnly: true,
                    minimap: { enabled: false },
                    fontSize: 16,
                    wordWrap: "on",
                    scrollBeyondLastLine: false,
                    automaticLayout: true,
                    scrollbar: {
                      horizontal: "auto",
                      vertical: "auto",
                    },
                  }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CodeCompare;