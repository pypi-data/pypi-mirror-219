import yaml
from pathlib import Path
def CreatePhenopacket(id:str, sex :str, hpos :list[dict], hts_file, ymlfile, owner, date):
  yml_path = Path(ymlfile)
  if yml_path.exists():
     yml_path.unlink()  
  cfg = {'id': id,
 'subject': {'id': id, 'sex': sex.upper()},
 'phenotypicFeatures': [{'type': {'id': hpo['id'], 'label': hpo['label']}} for hpo in hpos],
 'htsFiles': [{'uri': hts_file,
   'htsFormat': 'VCF',
   'genomeAssembly': 'hg19'}],
 'metaData': {'created': date,
  'createdBy': owner,
  'resources': [{'id': 'hp',
    'name': 'human phenotype ontology',
    'url': 'http://purl.obolibrary.org/obo/hp.owl',
    'version': 'hp/releases/2019-11-08',
    'namespacePrefix': 'HP',
    'iriPrefix': 'http://purl.obolibrary.org/obo/HP_'}],
  'phenopacketSchemaVersion': 1.0}}
  with open (ymlfile, 'w') as yml:
     yaml.dump(cfg,yml)
  return {
        'status':1,
        'message': 'Created successfully'
    }

def CreateAnalysis(proband :str , vcf:str, hpos: list[str], ymlfile: str,outfile, ped:str = ''):
  yml_path = Path(ymlfile)
  if yml_path.exists():
        yml_path.unlink()
  outpaht = Path(outfile)
  outpaht.parent.mkdir(parents=True, exist_ok=True)
  cfg = {
          'analysis':{
              'genomeAssembly': 'hg19',
              'vcf':vcf,
              'ped': ped,
              'proband': proband,
              'hpoIds':hpos,
              'inheritanceModes': {
                  'AUTOSOMAL_DOMINANT': 0.1,
                  'AUTOSOMAL_RECESSIVE_HOM_ALT': 0.1,
                  'AUTOSOMAL_RECESSIVE_COMP_HET': 2.0,
                  'X_DOMINANT': 0.1,
                  'X_RECESSIVE_HOM_ALT': 0.1,
                  'X_RECESSIVE_COMP_HET': 2.0,
                  'MITOCHONDRIAL': 0.2
                },
              'analysisMode': 'PASS_ONLY',
              'frequencySources': [
          'THOUSAND_GENOMES',
          'TOPMED',
          'UK10K',
          'ESP_AFRICAN_AMERICAN', 'ESP_EUROPEAN_AMERICAN', 'ESP_ALL',
          'EXAC_AFRICAN_INC_AFRICAN_AMERICAN', 'EXAC_AMERICAN',
          'EXAC_SOUTH_ASIAN', 'EXAC_EAST_ASIAN',
          'EXAC_FINNISH', 'EXAC_NON_FINNISH_EUROPEAN',
          'EXAC_OTHER',
          'GNOMAD_E_AFR',
          'GNOMAD_E_AMR',
          'GNOMAD_E_EAS',
          'GNOMAD_E_FIN',
          'GNOMAD_E_NFE',
          'GNOMAD_E_OTH',
          'GNOMAD_E_SAS',
          'GNOMAD_G_AFR',
          'GNOMAD_G_AMR',
          'GNOMAD_G_EAS',
          'GNOMAD_G_FIN',
          'GNOMAD_G_NFE',
          'GNOMAD_G_OTH',
          'GNOMAD_G_SAS'
      ],
      'pathogenicitySources': [ 'REVEL', 'MVP' ],
      'steps':[
          {'failedVariantFilter': {}},
        { 'variantEffectFilter': {
              'remove':[
                'FIVE_PRIME_UTR_EXON_VARIANT',
                'FIVE_PRIME_UTR_INTRON_VARIANT',
                'THREE_PRIME_UTR_EXON_VARIANT',
                'THREE_PRIME_UTR_INTRON_VARIANT',
                'NON_CODING_TRANSCRIPT_EXON_VARIANT',
                'NON_CODING_TRANSCRIPT_INTRON_VARIANT',
                'CODING_TRANSCRIPT_INTRON_VARIANT',
                'UPSTREAM_GENE_VARIANT',
                'DOWNSTREAM_GENE_VARIANT',
                'INTERGENIC_VARIANT',
                'REGULATORY_REGION_VARIANT'

              ],
          }},
          {'frequencyFilter': {'maxFrequency': 2.0}},
          {'pathogenicityFilter': {'keepNonPathogenic': True}},
          {'inheritanceFilter': {}},
        { 'omimPrioritiser': {}},
          {'hiPhivePrioritiser': {}},
      ],},
      'outputOptions':{
          'outputContributingVariantsOnly': False,
          'numGenes': 0,
          'outputFileName': outfile,
          'outputFormats': ['JSON', 'TSV_GENE', 'TSV_VARIANT']}
      }
  with open (ymlfile, 'w') as yml:
    yaml.dump(cfg,yml)
  return {
          'status':1,
          'message': 'Created successfully'
      }
