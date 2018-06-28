def display_file(buffered_data):
    # Process buffered data
    if buffered_data and buffered_data.startswith('HTTP/1.1 400'):
        print 'Invalid URL!! File name is required'
    else:
        header_data, file_data = buffered_data.split('\n\n', 1)
        # print header_data # Printing more data
        with open('received_file', 'wb') as f:
            # write data to a file
            f.write(file_data)
            f.close()
            print('File has been saved successfully.')