import subprocess
from exomIO import CreateAnalysis
def run_subprocess(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
        status = 1
        return_code = 1
        message = "Subprocess completed successfully."
        outlog = output
    except subprocess.CalledProcessError as e:
        message = "Subprocess encountered an error."
        status = 0
        return_code =  e.returncode
        outlog =  e.output
    return {
        'status' : status,
        'return_code': return_code,
        'message': message,
        'outlog' : outlog
    }
def launch(exomiser_path, analysis_path, config_path, vcf, hpos, outfile, ped = '', proband = ''):
    command  = f'java -Xmx4g -jar {exomiser_path} --analysis {analysis_path} --spring.config.location={config_path}'
    analysis = CreateAnalysis(proband=proband, hpos=hpos, outfile=outfile, ped=ped, vcf=vcf, ymlfile=analysis_path)
    if analysis['status'] == 1:
        out = run_subprocess(command=command)
        if out['status'] == 1:
            return True
        else:
            return False
    else:
        return False