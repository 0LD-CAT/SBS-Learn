const Task = ({ block }) => {
  return (
    <div className="bg-white rounded-2xl shadow p-6">
      <h3 className="text-xl font-semibold mb-2">{block.title}</h3>

      <p className="mb-4 text-gray-700">{block.description}</p>

      <div className="bg-gray-100 p-3 rounded-lg mb-3">
        <b>Ожидаемый вывод:</b> {block.expected_output}
      </div>

      <div className="text-sm text-gray-500">
        💡 {block.hint}
      </div>
    </div>
  );
};

export default Task;