function extract(audio_file, output_file)

[features, feature_names] = voice_analysis(audio_file)
fid = fopen(output_file, 'wt');
fprintf(fid, '%f\n', features);
fclose(fid);
exit;