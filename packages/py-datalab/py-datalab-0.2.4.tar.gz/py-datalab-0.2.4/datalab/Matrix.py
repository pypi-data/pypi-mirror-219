from datalab.utils import *


class Matrix:
    @overload
    def __init__(
        self,
        rows: int,
        columns: int,
        dtype: type = int,
        fill: Union[int, float, str, bool] = 0,
    ) -> None:
        """Initializes a new matrix with the specified number of rows and columns.

        Parameters
        ----------
        rows : int
            The number of rows in the matrix.
        columns : int
            The number of columns in the matrix.
        dtype : type, optional
            The data type of the matrix elements (default: int).
        fill : Union[int, float, str, bool], optional
            The value used to fill the matrix elements (default: 0)"""

        pass

    @overload
    def __init__(
        self,
        shape: tuple[int, int],
        dtype: type = int,
        fill: Union[int, float, str, bool] = 0,
    ) -> None:
        """Initializes a new matrix with the specified shape.

        Parameters
        ----------
        shape : tuple[int, int]
            The shape of the matrix, specified as a tuple (rows, columns).
        dtype : type, optional
            The data type of the matrix elements (default: int).
        fill : Union[int, float, str, bool], optional
            The value used to fill the matrix elements (default: 0)"""

        pass

    @overload
    def __init__(
        self,
        object: Iterable,
        dtype: type = int,
    ) -> None:
        """Initializes a new matrix from an iterable object.

        Parameters
        ----------
        object : Iterable
            An iterable object containing the matrix elements
        dtype : type, optional
            The data type of the matrix elements (default: int)"""

        pass

    def __init__(
        self,
        arg1: Optional[Union[Iterable, tuple[int, int]]] = None,
        arg2: Optional[Union[int, type]] = None,
        dtype: Optional[type] = int,
        fill: Optional[Union[int, float, str, bool]] = 0,
    ) -> None:
        if (
            isinstance(arg1, tuple)
            and len(arg1) == 2
            and (isinstance(arg1[0], int) and isinstance(arg1[1], int))
        ):
            self._initialize_data_structure(shape=arg1, dtype=dtype, fill=fill)

        elif isinstance(arg1, int) and isinstance(arg2, int):
            self._initialize_data_structure(shape=(arg1, arg2), dtype=dtype, fill=fill)

        elif isinstance(arg1, (list, tuple)) and all(
            isinstance(sublist, (list, tuple)) for sublist in arg1
        ):
            self._initialize_data_structure(object=arg1, dtype=dtype)

        else:
            raise ValueError("Wrong parameters in Matrix initialization")

        self.__precision = 4
        self.__supported_types = int, float, str, bool

    def __str__(self) -> str:
        buffer = [[" " for _ in range(self.columns)] for _ in range(self.rows)]

        for i, row in enumerate(self.__data):
            for j, value in enumerate(row):
                if self.dtype == float:
                    splited_value = str(value).split(".")

                    if len(splited_value) == 1:
                        if splited_value[0] == "0":
                            formatted_value = f"0."

                        else:
                            formatted_value = f"{splited_value[0]}."

                    if len(splited_value) == 2:
                        if splited_value[0] == "0" and splited_value[1] == "0":
                            formatted_value = f"0."

                        elif splited_value[0] == "0" and splited_value[1] != "0":
                            if len(splited_value[1]) > self.__precision:
                                formatted_value = "{:.{}e}".format(
                                    value, self.__precision
                                )
                            else:
                                formatted_value = f"0.{splited_value[1]}"

                        elif splited_value[0] != "0" and splited_value[1] == "0":
                            formatted_value = f"{splited_value[0]}."

                        else:
                            if len(splited_value[1]) > self.__precision:
                                formatted_value = "{:.{}e}".format(
                                    value, self.__precision
                                )
                            else:
                                formatted_value = (
                                    f"{splited_value[0]}.{splited_value[1]}"
                                )

                elif self.dtype == int:
                    formatted_value = str(value)

                elif self.dtype == bool:
                    formatted_value = str(value)

                else:
                    formatted_value = f"'{str(value)}'"

                buffer[i][j] = formatted_value

        max_element_lengths = tuple(
            max(len(str(row[i])) for row in buffer) for i in range(len(buffer[0]))
        )

        output = "\n"

        for row in buffer:
            output += "│ "

            for value, max_length in zip(row, max_element_lengths):
                output += f"{value}{' ' * (max_length - len(value) + 1)}"

            output += "│\n"

        return output

    def __setitem__(
        self, index: Union[tuple, int], value: Union[list, int, float, str, bool]
    ) -> None:
        if (
            isinstance(index, tuple)
            and isinstance(index[0], int)
            and isinstance(index[1], int)
            and len(index) == 2
        ):
            row, column = index
        elif isinstance(index, int):
            row = index
            column = None
        else:
            raise ValueError(
                "The index you are referring to must be of the form: object[int][int], or object[int, int]"
            )

        for supported_type in self.__supported_types:
            if self.dtype == supported_type:
                converted_value = supported_type(value)
                break

        if column is not None:
            self.__data[row][column] = converted_value
        else:
            self.__data[row] = converted_value

    def __getitem__(
        self, index: Union[tuple, int]
    ) -> Union[list, int, float, str, bool]:
        if (
            isinstance(index, tuple)
            and isinstance(index[0], int)
            and isinstance(index[1], int)
            and len(index) == 2
        ):
            rows, columns = index
            return self.__data[rows][columns]

        elif isinstance(index, int):
            return self.__data[index]

        else:
            raise ValueError(
                "The index you are referring to must be of the form: object[int][int], or object[int, int]"
            )

    def __add__(self, element: Iterable) -> Self:
        def matrix_addition(A: Iterable, B: Iterable) -> Iterable:
            return [[a + b for a, b in zip(row1, row2)] for row1, row2 in zip(A, B)]

        buffer = self.deep_copy()

        if isinstance(element, Matrix):
            if buffer.shape == element.shape:
                buffer.__data = matrix_addition(self.__data, element)
            else:
                raise ArithmeticError("Cannot add matrices with different shapes")

        elif isinstance(element, (list, tuple)):
            if len(element) != buffer.rows or any(
                len(row) != buffer.columns for row in element
            ):
                raise ArithmeticError("Cannot add matrices with different shapes")

            buffer.__data = matrix_addition(buffer.__data, element)

        else:
            raise ValueError(
                "You can only add matrix to another matrix, list, or tuple"
            )

        return buffer

    def __sub__(self, element: Iterable) -> Self:
        def matrix_subtraction(A: Iterable, B: Iterable) -> Iterable:
            return [[a - b for a, b in zip(row1, row2)] for row1, row2 in zip(A, B)]

        buffer = self.deep_copy()

        if isinstance(element, Matrix):
            if buffer.shape == element.shape:
                buffer.__data = matrix_subtraction(buffer.__data, element)
            else:
                raise ArithmeticError("Cannot subtract matrices with different shapes")

        elif isinstance(element, (list, tuple)):
            if len(element) != buffer.rows or any(
                len(row) != buffer.columns for row in element
            ):
                raise ArithmeticError("Cannot subtract matrices with different shapes")

            buffer.__data = matrix_subtraction(buffer.__data, element)

        else:
            raise ValueError(
                "You can only subtract a matrix from another matrix, list, or tuple"
            )

        return buffer

    def __mul__(self, element: Iterable) -> Self:
        buffer = self.deep_copy()

        if isinstance(element, Matrix):
            if buffer.columns != element.rows:
                raise ArithmeticError(
                    "Cannot multiply matrices with incompatible dimensions"
                )
            buffer.__data = [
                [
                    sum(a * b for a, b in zip(row1, col2))
                    for col2 in zip(*element.__data)
                ]
                for row1 in buffer.__data
            ]

        elif isinstance(element, (list, tuple)):
            if buffer.columns != len(element):
                raise ArithmeticError(
                    "Cannot multiply matrices with incompatible dimensions"
                )

            buffer.__data = [
                [sum(a * b for a, b in zip(row1, col2)) for col2 in zip(*element)]
                for row1 in buffer.__data
            ]

        elif isinstance(element, (int, float, str, bool)):
            buffer.__data = [[element * a for a in row] for row in buffer.__data]

        else:
            raise ValueError("Invalid operand for matrix multiplication")

        return buffer

    def __pow__(self, exponent: int) -> Self:
        buffer = self.deep_copy()

        if not isinstance(exponent, int):
            raise ValueError(
                "Matrix exponentiation is only supported for integer exponents"
            )

        if exponent < 0:
            raise ValueError(
                "Matrix exponentiation is not supported for negative exponents"
            )

        if exponent == 0:
            if self.rows != self.columns:
                raise ValueError(
                    "Identity matrix must have same rows and columns number"
                )

            return Matrix(
                [
                    [1 if i == j else 0 for j in range(self.rows)]
                    for i in range(self.rows)
                ],
                dtype=self.dtype,
            )

        for _ in range(exponent - 1):
            buffer *= self

        return buffer

    def _fill_data(
        self,
        object: Optional[Iterable] = None,
        fill: Optional[Union[int, float, str, bool]] = None,
    ) -> None:
        empty_element = self._empty_element() if fill is None else fill

        self.__data = [
            [empty_element for _ in range(self.columns)] for _ in range(self.rows)
        ]

        if object is not None:
            for i, row in enumerate(object):
                for j, element in enumerate(row):
                    try:
                        self.__data[i][j] = element
                    except IndexError:
                        self.__data[i][j] = empty_element

    def _empty_element(self) -> Union[int, float, str, bool]:
        if self.dtype == float:
            return 0.0

        elif self.dtype == str:
            return ""

        elif self.dtype == bool:
            return False

        else:
            return 0

    def _initialize_data_structure(
        self,
        object: Optional[Iterable] = None,
        shape: Optional[tuple[int, int]] = None,
        dtype: Optional[type] = None,
        fill: Optional[Union[int, float, str, bool]] = None,
    ) -> None:
        if object is not None:
            rows_count = len(object)
            buffer = [0 for _ in range(rows_count)]

            for i, row in enumerate(object):
                buffer[i] = len(row)

            self.__rows = rows_count
            self.__columns = max(buffer)
            self.__dtype = self._estimate_data_type(object)
            self._fill_data(object)

        elif shape is not None:
            self.__rows, self.__columns = shape
            self.__dtype = dtype
            self._fill_data(fill=fill)

        else:
            raise ValueError(
                "Matrix._initilize_data_structure() has recived wrong parameters"
            )

    def _estimate_data_type(self, object: Iterable) -> type:
        type_counts = {int: 0, float: 0, str: 0, bool: 0}

        for row in object:
            for element in row:
                if isinstance(element, int):
                    type_counts[int] += 1
                elif isinstance(element, float):
                    type_counts[float] += 1
                elif isinstance(element, str):
                    type_counts[str] += 1
                elif isinstance(element, bool):
                    type_counts[bool] += 1

        if type_counts[int] > 0 and type_counts[float] > 0:
            return float
        else:
            return max(type_counts, key=type_counts.get)

    @property
    def size(self) -> int:
        """Number of elements in matrix"""

        return self.rows * self.columns

    @property
    def shape(self) -> tuple[int, int]:
        """Store current matrix shape"""

        return self.rows, self.columns

    @shape.setter
    def shape(self, new_shape: tuple[int, int]) -> None:
        if isinstance(new_shape, tuple):
            self.rows, self.columns = new_shape
        else:
            raise ValueError("`dl.Matrix.shape` property must be a tuple of integers")

    @property
    def dtype(self) -> type:
        """Store element's current type"""

        return self.__dtype

    @dtype.setter
    def dtype(self, new_value: type) -> None:
        if new_value in (int, float, str, bool):
            self.__dtype = new_value
        else:
            raise ValueError("`dl.Matrix.dtype` property must be an type object")

    @property
    def columns(self) -> int:
        """Number of columns in matrix"""

        return self.__columns

    @columns.setter
    def columns(self, new_value: int) -> None:
        if isinstance(new_value, int):
            self.__columns = new_value
            self._adjust_dimensions()
        else:
            raise ValueError("`dl.Matrix.columns` property must be an integer")

    @property
    def rows(self) -> int:
        """Number of rows in matrix"""

        return self.__rows

    @rows.setter
    def rows(self, new_value: int) -> None:
        if isinstance(new_value, int):
            self.__rows = new_value
            self._adjust_dimensions()
        else:
            raise ValueError("`dl.Matrix.rows` property must be an integer")

    def _adjust_dimensions(self) -> None:
        buffer = self.__data.copy()

        init_item = self._empty_element()

        self.__data = [
            [init_item for _ in range(self.columns)] for _ in range(self.rows)
        ]

        for i in range(self.rows):
            for j in range(self.columns):
                try:
                    self.__data[i][j] = buffer[i][j]
                except:
                    continue

    @property
    def permanent(self) -> Union[int, float]:
        """The permanent of the matrix."""

        if self.rows != self.columns:
            raise ValueError("Permanent is only defined for square matrices.")

        if self.size == 1:
            return self.__data[0, 0]

        result = 0
        for permutation in self._permutations(range(self.rows)):
            product = 1
            for i, j in enumerate(permutation):
                product *= self[i, j]
            result += product

        return result

    def _permutations(self, last: Iterable) -> Iterable:
        if len(last) == 1:
            yield last
        else:
            for i in range(len(last)):
                rest = list(last[:i]) + list(last[i + 1 :])
                for p in self._permutations(rest):
                    yield [last[i]] + p

    @property
    def determinant(self) -> Union[int, float]:
        """The determinant of the matrix"""

        if self.rows != self.columns:
            raise ValueError("Determinant is only defined for square matrices.")

        if self.size == 1:
            return self.__data[0][0]

        if self.rows == 2:
            return (
                self.__data[0][0] * self.__data[1][1]
                - self.__data[0][1] * self.__data[1][0]
            )

        result = 0
        for j in range(self.columns):
            submatrix = self.submatrix(
                range(1, self.rows),
                [column for column in range(self.columns) if column != j],
            )
            result += self.__data[0][j] * submatrix.determinant() * (-1) ** j

        return result

    @property
    def trace(self) -> Union[int, float]:
        """Calculates the trace of a square matrix.

        The trace of a square matrix is the sum of its diagonal elements."""

        if self.rows != self.columns:
            raise ValueError("Trace is only defined for square matrices.")

        return sum(self[i, i] for i in range(self.rows))

    def change_dtype(self, new_dtype: type) -> Self:
        """Changes the data type of the matrix.

        Parameters
        ----------
        new_dtype : type
            The new data type for the matrix"""

        self.dtype = new_dtype
        self._change_data_type(new_dtype)

        return self

    def _change_data_type(self, new_dtype: type) -> None:
        if new_dtype not in self.__supported_types:
            raise ValueError(
                f"dl.Matrix.dtype must take one of this value: {self.__supported_types}"
            )

        self.__data = [[new_dtype(element) for element in row] for row in self.__data]

    def fill(self, value: Union[int, float, str, bool]) -> Self:
        """Fills the matrix with the specified value.

        Parameters
        ----------
        value : int or float or str or bool
            Value to fill the matrix with"""

        if not has_same_type(self.dtype, value):
            value = convert(value, self.dtype)

        for i in range(self.rows):
            for j in range(self.columns):
                self.__data[i][j] = value

        return self

    def set_precision(self, new_precision: int) -> None:
        """Sets the precision for numerical values in the matrix.

        Parameters
        ----------
        new_precision : int
            The new precision value to set for numerical values.

        Raises
        ------
        ValueError
            If the provided precision is not an integer"""

        if isinstance(new_precision, int):
            self.__precision = new_precision
        else:
            raise ValueError("Number precision must be an integer")

    def is_identity(self) -> bool:
        """Checks if the current matrix is an identity matrix.

        Returns
        -------
        bool
            True if the matrix is an identity matrix, False otherwise"""

        if self.rows != self.columns:
            return False

        for i in range(self.rows):
            for j in range(self.rows):
                if i == j:
                    if self[i, j] != 1:
                        return False
                else:
                    if self[i, j] != 0:
                        return False

        return True

    def transpose(self) -> Self:
        """Transposes the matrix.

        The transpose of a matrix is obtained by interchanging its rows and columns.
        This operation modifies the matrix in place"""

        buffer = self.deep_copy()

        self.reshape(self.columns, self.rows)

        for i in range(self.rows):
            for j in range(self.columns):
                self[i, j] = buffer[j, i]

        return self

    def inverse(self) -> Self:
        """Calculates the inverse of a square matrix.

        Returns
        -------
        Matrix
            The inverse matrix.

        Raises
        ------
        ValueError
            If the matrix is not square or it is singular (non-invertible).

        Notes
        -----
        The matrix must be square and non-singular (invertible) to have an inverse."""

        if self.rows != self.columns:
            raise ValueError("Inverse is only defined for square matrices.")

        determinant = self.determinant

        if determinant == 0:
            raise ValueError("Matrix is singular and does not have an inverse.")

        adjugate = self.adjugate()

        return adjugate * (1 / determinant)

    def adjugate(self) -> Self:
        """Calculates the adjugate of the matrix.

        Raises
        ------
        ValueError
            If the matrix is not square."""

        if self.rows != self.columns:
            raise ValueError("Adjugate is only defined for square matrices.")

        cofactors = Matrix(self.shape)

        for i in range(self.rows):
            for j in range(self.columns):
                submatrix = self.submatrix(
                    [row for row in range(self.rows) if row != i],
                    [col for col in range(self.columns) if col != j],
                )
                cofactor = (-1) ** (i + j) * submatrix.determinant
                cofactors.__data[i][j] = cofactor

        return cofactors.transpose()

    def swap_rows(self, row1: int, row2: int) -> Self:
        """Swaps two rows in the matrix.

        Parameters
        ----------
        row1 : int
            Index of the first row to swap.
        row2 : int
            Index of the second row to swap."""

        self.__data[row1], self.__data[row2] = self.__data[row2], self.__data[row1]
        return self

    def scale_row(self, row: int, scalar: Union[int, float]) -> Self:
        """Scales a row in the matrix by a scalar value.

        Parameters
        ----------
        row : int
            Index of the row to scale.
        scalar : int or float
            Scalar value to multiply the row by."""

        self.__data[row] = [scalar * element for element in self.__data[row]]
        return self

    def submatrix(self, rows_index: Iterable, columns_index: Iterable) -> Self:
        """Creates and returns a submatrix by selecting the specified ranges of rows and columns.

        Parameters
        ----------
        rows_index : Iterable
            The range of row indices to include in the submatrix.
        columns_index : Iterable
            The range of column indices to include in the submatrix.

        Returns
        -------
        Matrix
            The submatrix with the specified ranges of rows and columns.

        Notes
        -----
        This method creates a new matrix object with dimensions (len(rows_index), len(columns_index)),
        where the rows and columns within the specified ranges are included. The elements of the submatrix
        are obtained from the corresponding elements of the original matrix."""

        sub_rows = len(rows_index)
        sub_columns = len(columns_index)
        submatrix = Matrix((sub_rows, sub_columns))

        for i, row_index in enumerate(rows_index):
            for j, column_index in enumerate(columns_index):
                submatrix.__data[i][j] = self.__data[row_index][column_index]

        return submatrix

    def to_lower_triangular(self) -> Self:
        """Converts the matrix to lower triangular form.

        Returns
        -------
        Matrix
            The matrix in lower triangular form.

        Notes
        -----
        In a lower triangular matrix, all elements above the main diagonal are set to 0.
        """

        result = self.deep_copy()

        for i in range(result.rows):
            for j in range(i + 1, result.columns):
                result.__data[i][j] = 0

        return result

    def to_upper_triangular(self) -> Self:
        """Converts the matrix to upper triangular form.

        Returns
        -------
        Matrix
            The matrix in upper triangular form.

        Notes
        -----
        In an upper triangular matrix, all elements below the main diagonal are set to 0.
        """

        result = self.deep_copy()

        for i in range(1, result.rows):
            for j in range(i):
                result.__data[i][j] = 0

        return result

    def to_logical_matrix(self) -> Self:
        """Convert current matrix to logical matrix ((0, 1)-matrix)

        This function change all elements in matrix to bool and from this it follows that the matrix becomes a logical matrix
        """

        self.change_dtype(bool)

        return self

    @overload
    def reshape(self, rows: int, columns: int) -> Self:
        """Reshapes the matrix to the specified number of rows and columns

        Parameters
        ----------
        rows : int
            The number of rows for the reshaped matrix
        columns : int
            The number of columns for the reshaped matrix"""

        pass

    @overload
    def reshape(self, new_shape: tuple[int, int]) -> Self:
        """Reshapes the matrix to the specified shape

        Parameters
        ----------
        new_shape : tuple[int, int]
            The new shape for the matrix"""

        pass

    def reshape(
        self,
        arg1: Optional[Union[tuple[int, int], int]] = None,
        arg2: Optional[int] = None,
    ) -> Self:
        if (
            arg2 is None
            and isinstance(arg1, tuple)
            and isinstance(arg1[0], int)
            and isinstance(arg1[1], int)
            and len(arg1) == 2
        ):
            self.rows, self.columns = arg1
            self._adjust_dimensions()

        elif isinstance(arg1, int) and isinstance(arg2, int):
            self.rows, self.columns = arg1, arg2
            self._adjust_dimensions()

        else:
            raise ValueError(
                "Shape must be tuple of integers, or both rows and columns must be integers"
            )

        return self

    def to_list(self) -> list[list[Union[int, float, str, bool]]]:
        """Converts the matrix to a Python list"""

        return self.__data

    def to_tuple(self) -> tuple[tuple[Union[int, float, str, bool]]]:
        """Converts the matrix to a Python tuple"""

        buffer = [tuple() for _ in range(self.rows)]

        for i, row in enumerate(self.__data):
            buffer[i] = tuple(row)

        return tuple(buffer)

    def copy(self) -> Self:
        """Creates a copy of the matrix"""

        return copy.copy(self)

    def deep_copy(self) -> Self:
        """Creates a deep copy of the matrix"""

        return copy.deepcopy(self)
