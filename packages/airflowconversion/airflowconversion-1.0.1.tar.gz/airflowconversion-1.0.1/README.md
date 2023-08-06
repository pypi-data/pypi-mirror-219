## Python Utility tool for migration of workflows from Oozie to Airflow

- <b>Inputs required :</b>
1. Input folder path (Where the XML files to be converted are stored.)
2. Output folder path (Where the converted python files are to be stored)
3. Queue name (for the DAG)

<b>How to use this library:</b>
> from airflowconversion.ParseXML import conversion <br/>
conversion(r"<input_folder_path>", r"<output_folder_path>",'<queue_name>')