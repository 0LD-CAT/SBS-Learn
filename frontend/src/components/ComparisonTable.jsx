const ComparisonTable = ({ block, langs }) => {
  const langMap = {
    [langs.left.slug]: langs.left,
    [langs.right.slug]: langs.right,
  };

  return (
    <div className="bg-white rounded-2xl shadow p-6">
      <h3 className="text-xl font-semibold mb-4">
        {block.title}
      </h3>

      <div className="overflow-x-auto border border-primary">
        <table className="w-full border-collapse">
          {/* HEADER */}
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-green-300 px-4 py-3 text-left text-sm font-semibold">
                Параметр
              </th>

              {block.languages.map((lang) => {
                const langData = langMap[lang];

                return (
                  <th
                    key={lang}
                    className="border border-green-300 px-4 py-3 text-left font-semibold"
                  >
                    <div className="flex items-center gap-2">
                      {langData?.icon_url && (
                        <img
                          src={langData.icon_url}
                          className="w-5 h-5"
                        />
                      )}

                      <span>
                        {langData?.name || lang}
                      </span>
                    </div>
                  </th>
                );
              })}
            </tr>
          </thead>

          {/* BODY */}
          <tbody>
            {block.rows.map((row, i) => (
              <tr key={i} className="hover:bg-gray-50 transition">
                {/* ATTRIBUTE */}
                <td className="border border-green-300 px-4 py-3 font-medium text-gray-800 bg-gray-50">
                  {row.attribute}
                </td>

                {/* VALUES */}
                {block.languages.map((lang) => (
                  <td
                    key={lang}
                    className="border border-green-300 px-4 py-3 text-gray-700"
                  >
                    {row.values[lang]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ComparisonTable;