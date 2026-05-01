const FactBlock = ({ block, langs }) => {
  if (!langs) return null;

  const left = block[langs.left.slug];
  const right = block[langs.right.slug];

  return (
    <div className="grid md:grid-cols-2 gap-4">

      {/* LEFT LANGUAGE */}
      <div className="bg-green-50 border border-primary rounded-xl p-5">
        <div className="flex items-center gap-2 mb-3">
          <img
            src={langs.left.icon_url}
            alt={langs.left.name}
            className="w-10 h-10"
          />
        </div>

        <p className="text-black-900 leading-relaxed">
          {left?.content}
        </p>
      </div>

      {/* RIGHT LANGUAGE */}
      <div className="bg-red-50 border border-red-500 rounded-xl p-5">
        <div className="flex items-center gap-2 mb-3">
          <img
            src={langs.right.icon_url}
            alt={langs.right.name}
            className="w-10 h-10"
          />
        </div>

        <p className="text-black-900 leading-relaxed">
          {right?.content}
        </p>
      </div>

    </div>
  );
};

export default FactBlock;