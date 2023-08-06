import nemo
import nemo.collections.nlp as nemo_nlp
nmt_model = nemo_nlp.models.machine_translation.MTEncDecModel.from_pretrained(model_name="mnmt_deesfr_en_transformer12x2")
translations = nmt_model.translate(["Hallo, schön dich kennen zu lernen!"], source_lang="de", target_lang="en")