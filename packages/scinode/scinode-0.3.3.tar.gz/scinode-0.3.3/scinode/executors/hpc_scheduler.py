# Define possible parameters for each scheduler
scheduler_parameters = {
    "slurm": {
        "job_name": "#SBATCH --job-name={job_name}",
        "output": "#SBATCH --output={job_name}_slurm.out",
        "error": "#SBATCH --error={job_name}_slurm.err",
        "nodes": "#SBATCH --nodes={nodes}",
        "ntasks_per_node": "#SBATCH --ntasks-per-node={cpus}",
        "time": "#SBATCH --time={time}",
        "account": "#SBATCH --account={account}",
        "qos": "#SBATCH --qos={qos}",
        "partition": "#SBATCH --partition={partition}",
        "mem": "#SBATCH --mem={mem}",
        "additional_parameters": "{additional_parameters}",
    },
    "pbs": {
        "job_name": "#PBS -N {job_name}",
        "output": "#PBS -o {job_name}_pbs.out",
        "error": "#PBS -e {job_name}_pbs.err",
        "nodes": "#PBS -l nodes={nodes}:ppn={cpus}",
        "time": "#PBS -l walltime={time}",
        "account": "#PBS -A {account}",
        "qos": "#PBS -q {qos}",
        "partition": "#PBS -q {partition}",
        "mem": "#PBS -l mem={mem}",
        "additional_parameters": "{additional_parameters}",
    },
    "sge": {
        "job_name": "#$ -N {job_name}",
        "output": "#$ -o {job_name}_sge.out",
        "error": "#$ -e {job_name}_sge.err",
        "cpus": "#$ -pe smp {cpus}",
        "time": "#$ -l h_rt={time}",
        "account": "#$ -P {account}",
        "qos": "#$ -q {qos}",
        "partition": "#$ -q {partition}",
        "mem": "#$ -l mem={mem}",
        "additional_parameters": "{additional_parameters}",
    },
}


class SubmissionScriptGenerator:

    script_name = "submission.sh"

    def __init__(
        self,
        type="direct",
        job_name="scinode",
        nodes=1,
        cpus=1,
        time=None,
        account=None,
        qos=None,
        partition=None,
        mem=None,
        additional_parameters=None,
        **kwargs,
    ):
        self.type = type
        self.job_name = job_name
        self.nodes = nodes
        self.cpus = cpus
        self.time = time
        self.account = account
        self.qos = qos
        self.partition = partition
        self.mem = mem
        self.additional_parameters = additional_parameters
        self.script_lines = []

    def add_line(self, line):
        self.script_lines.append(line)

    def generate_script(self):
        script = ""
        if self.type in scheduler_parameters:
            script += "#!/bin/bash\n"
            for _param, value in scheduler_parameters[self.type].items():
                key = value.split("{")[1].split("}")[0]
                param_value = getattr(self, key, None)
                if param_value is not None:
                    script += value.format(**vars(self)) + "\n"
            script += "\n".join(self.script_lines)
        else:  # Direct execution
            script += "\n".join(self.script_lines)

        return script


if __name__ == "__main__":
    # Example usage:
    generator = SubmissionScriptGenerator(
        type="slurm",
        nodes=2,
        cpus=4,
        time="01:00:00",
        account="my_account",
        qos="high",
        additional_parameters="--gres=gpu:1",
    )
    generator.add_line('echo "Hello, World!"')
    script_content = generator.generate_script()
    print(script_content)
