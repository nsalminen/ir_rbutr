from pyrouge import Rouge155

for system_id in ['fluoridation', 'gerson', 'thyroid']:
    rouge = Rouge155()
    rouge.system_dir = 'absolute path to/ir_rbutr/Evaluation/system_summaries/' + system_id
    rouge.model_dir = 'absolute path to/ir_rbutr/Evaluation/model_summaries/' + system_id
    rouge.system_filename_pattern = 'summary' + '.(\d+).txt'
    rouge.model_filename_pattern = 'summary' + '.[A-Z].#ID#.txt'
    output = rouge.convert_and_evaluate(system_id, True)
    file = open("absolute path to/ir_rbutr/Evaluation/out/" + system_id + ".001.txt", 'w')
    file.write(str(output))
    print(output)
