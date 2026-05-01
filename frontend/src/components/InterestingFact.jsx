const InterestingFact = ({ block, langs }) => {
  const left = block[langs.left.slug];
  const right = block[langs.right.slug];

  return (
    <div className="bg-white border border-primary rounded-2xl p-6 shadow-sm">

      {/* HEADER */}
      <div className="flex items-center gap-2 mb-4">
        <div className="text-primary text-xl">💡</div>

        <h3 className="font-semibold text-primary">
          Интересный факт
        </h3>
      </div>

      {/* CONTENT */}
      <div className="grid md:grid-cols-2 gap-4">

        {/* LEFT LANGUAGE */}
        <div className="bg-white/70 rounded-xl p-4 border border-green-300">
          <div className="text-sm font-medium text-primary mb-2 flex items-center gap-2">
            <img
              src={langs.left.icon_url}
              className="w-4 h-4"
              alt=""
            />
            {langs.left.name}
          </div>

          <p className="text-gray-700 leading-relaxed">
            {left?.content}
          </p>
        </div>

        {/* RIGHT LANGUAGE */}
        <div className="bg-white/70 rounded-xl p-4 border border-red-300">
          <div className="text-sm font-medium text-primary mb-2 flex items-center gap-2">
            <img
              src={langs.right.icon_url}
              className="w-4 h-4"
              alt=""
            />
            {langs.right.name}
          </div>

          <p className="text-gray-700 leading-relaxed">
            {right?.content}
          </p>
        </div>

      </div>
    </div>
  );
};

export default InterestingFact;