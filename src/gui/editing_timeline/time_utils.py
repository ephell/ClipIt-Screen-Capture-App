class TimeUtils:

    @staticmethod
    def calculate_timestamp_by_handle_position(
        delta_x, 
        handle_x, 
        max_x, 
        min_x, 
        max_possible_duration
    ):
        """
        Returns
        ----------
        timestamp : float
            The timestamp calculated from the handle position (in ms).
        """
        handle_range = max_x - min_x
        handle_position = handle_x - min_x + delta_x
        time_ratio = handle_position / handle_range
        timestamp = time_ratio * max_possible_duration
        if timestamp > max_possible_duration:
            timestamp = max_possible_duration
        elif timestamp < 0:
            timestamp = 0
        return timestamp
    
    @staticmethod
    def format_timestamp(timestamp):
        """
        Parameters
        ----------
        timestamp : float/int
            The timestamp to format (in ms).
        """
        milliseconds = int(timestamp)
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
