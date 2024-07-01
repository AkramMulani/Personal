
from matplotlib import pyplot as plt


class Extractor:
    def __init__(self, file_path):
        self.lines = []
        self.data = dict()
        self.time_list = []
        self.data_list = []
        with open(file_path, "r") as log_file:
            for line in log_file:
                self.lines.append(line)

    def extract_data(self):
        self.process_lines()
        self.data['data'] = self.data_list
        self.data['time'] = self.time_list
        return self.data

    def process_lines(self):
        for line in self.lines:
            is_payload = str(line).find('payload')
            is_data_msg_event = str(line).find('PubSub::DataMessageEvent')
            if is_data_msg_event != -1:
                try:
                    data_msg_event = str(line).split('PubSub::DataMessageEvent')[1]
                    data_dict = self.create_dict(data_msg_event)
                    self.data_list.append(data_dict)
                    # print(data_dict)
                except Exception:
                    pass
            if is_payload != -1:
                try:
                    payload = line.split('payload')[1]
                    new_payload = str(payload).replace('=', "").replace('"', '').replace("}", "")
                    time_in_ns = int(new_payload.split('time')[1].strip().split(' ')[-1])
                    if time_in_ns >= 0 and self.time_list.count(str(time_in_ns)) < 1:
                        self.time_list.append(str(time_in_ns))
                    # print(time_is_ns)
                except Exception:
                    pass
        print(self.time_list)
        print(self.data_list)

    def create_dict(self, data_msg_event):
        # {data=9a 99 99 99 99 99 c9 3f, size=8}
        l1 = data_msg_event.replace('{', '').replace('}', '').split(',')
        data = l1[0].replace('data=', '')
        size = l1[1].replace('size=', '').strip()
        dictionary = {'data': data, 'size': size}
        return dictionary


def plot_data_vs_time(data_list, time_list):
    """
      Plots received and sent data vs time in nanoseconds on a single plot.

      Args:
        data_list: A list containing received and sent data (strings in hex format).
        time_list: A list containing corresponding times in nanoseconds.
    """
    print(data_list)
    print(time_list)
    received_data = []
    sent_data = []

    for data in data_list:
        print(data)
        if int(data['size']) == 1:
            sent_data.append(data['data'])
        if int(data['size']) == 8:
            received_data.append(data['data'])

    # Check if data lengths match time list
    if len(received_data) != len(sent_data) != len(time_list):
        raise ValueError("Unequal lengths in data lists and time list.")

    print('Lengths:')
    print(f'Received data list length: {len(received_data[1:])}')
    print(f'Sent data list length: {len(sent_data)}')
    print(f' Time list length: {len(time_list)}')
    # Create the plot
    plt.figure(figsize=(10, 6))  # Adjust figure size as needed
    plt.plot(time_list, received_data[1:], label="Received Data", marker='o')
    plt.plot(time_list, sent_data, label="Sent Data", marker='s')
    plt.xlabel("Time (ns)")
    plt.ylabel("Data Value")
    plt.title("Received and Sent Data vs Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    executor = Extractor('dspace_logs.txt')
    data = executor.extract_data()
    plot_data_vs_time(data['data'], data['time'])
