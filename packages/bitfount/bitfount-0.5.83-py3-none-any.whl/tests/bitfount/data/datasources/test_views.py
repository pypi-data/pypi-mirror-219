"""Tests for view datasources."""
import datetime
import os
from pathlib import Path
import platform
import sqlite3
from typing import Generator, List, MutableMapping, Union, cast
from unittest.mock import Mock, create_autospec

import numpy as np
import pandas as pd
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
import pytest
from pytest import fixture
from pytest_mock import MockerFixture

from bitfount import BitfountSchema
from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.csv_source import CSVSource
from bitfount.data.datasources.dicom_source import DICOMSource
from bitfount.data.datasources.views import (
    DropColsDataview,
    DropColViewConfig,
    SQLDataView,
    SQLViewConfig,
)
from bitfount.data.exceptions import SQLViewError
from bitfount.data.types import _ForceStypeValue, _SemanticTypeValue, _SingleOrMulti
from bitfount.federated.pod_db_utils import _sql_type_name
from tests.utils.helper import create_datasource, unit_test

POD_NAME = "testpod"
POD_NAME_DICOM = "DICOMtestpod"


@fixture
def dataframe() -> pd.DataFrame:
    """Simple dataframe for testing.

    Creates a simple 5-column dataframe with a bunch of different dtypes.
    """
    df = pd.DataFrame(
        {
            "int_column": [1, 2, 3],
            "float_column": [1.0, 2.0, 3.0],
            "str_column": ["1", "2", "3"],
        }
    )
    df["date"] = datetime.date(2020, 1, 1)
    df["datetime"] = datetime.datetime(2020, 1, 1, 0, 0)
    return df


@unit_test
class TestDropColsDataview:
    """Tests for the DropColsDataview class."""

    @fixture
    def mock_csv_datasource(self, dataframe: pd.DataFrame) -> Mock:
        """A mock CSV Datasource instance for view testing.

        Dataframe will be preset on this mock.
        """
        mock_csv_datasource: Mock = create_autospec(CSVSource, instance=True)
        mock_csv_datasource.data_splitter = None
        # Need to directly replace get_data to avoid issues with methodtools.lru_cache
        mock_csv_datasource.get_data = Mock(return_value=dataframe)
        return mock_csv_datasource

    @fixture
    def columns_to_drop(self) -> List[str]:
        """Columns to drop in the view."""
        return ["int_column", "date"]

    @fixture
    def dropped_cols_view(
        self, columns_to_drop: List[str], mock_csv_datasource: Mock
    ) -> DropColsDataview:
        """The view datasource with columns dropped."""
        return DropColsDataview(mock_csv_datasource, columns_to_drop)

    @pytest.mark.parametrize(
        "cols_to_drop", ("single_col", ("multiple", "cols")), ids=("single", "multiple")
    )
    def test_drop_col_view_parses_single_multi_cols(
        self, cols_to_drop: _SingleOrMulti[str], mock_csv_datasource: Mock
    ) -> None:
        """Test that class can be created with single or multiple columns."""
        drop_cols_view = DropColsDataview(mock_csv_datasource, cols_to_drop)

        # Should be converted to a list for internal storage either way
        assert isinstance(drop_cols_view._drop_cols, list)
        # Single column case:
        if isinstance(cols_to_drop, str):
            assert len(drop_cols_view._drop_cols) == 1
            assert drop_cols_view._drop_cols[0] == cols_to_drop
        # Multiple columns case:
        else:
            assert len(drop_cols_view._drop_cols) == len(cols_to_drop)
            assert drop_cols_view._drop_cols == list(cols_to_drop)

    def test_get_data(self, dropped_cols_view: DropColsDataview) -> None:
        """Test that get_data returns a dataframe with dropped columns."""
        expected_df = pd.DataFrame(
            {
                "float_column": [1.0, 2.0, 3.0],
                "str_column": ["1", "2", "3"],
            }
        )
        expected_df["datetime"] = datetime.datetime(2020, 1, 1, 0, 0)

        data = dropped_cols_view.get_data()

        assert data.equals(expected_df)

    def test_get_values(self, dropped_cols_view: DropColsDataview) -> None:
        """Test that get_values works as expected."""
        expected_values = {
            "float_column": [1.0, 2.0, 3.0],
            "str_column": ["1", "2", "3"],
            "datetime": [pd.to_datetime(datetime.datetime(2020, 1, 1, 0, 0))],
        }

        values = dropped_cols_view.get_values(
            ["float_column", "str_column", "datetime"]
        )

        # Check that these and only these columns are present
        assert expected_values.keys() == values.keys()
        for i in expected_values:
            assert list(values[i]) == expected_values[i]

    def test_get_values_dropped_column(
        self, dropped_cols_view: DropColsDataview
    ) -> None:
        """Test that error raised if get_values requests a dropped column."""
        with pytest.raises(KeyError):
            dropped_cols_view.get_values(["int_column"])

        # Check that the "dropped column" was in the underlying data
        assert "int_column" in cast(
            pd.DataFrame, dropped_cols_view._datasource.get_data()
        )

    def test_get_column(self, dropped_cols_view: DropColsDataview) -> None:
        """Test that get_column works as expected."""
        expected_col = pd.Series([1.0, 2.0, 3.0])

        col = dropped_cols_view.get_column("float_column")

        assert cast(pd.Series, col).equals(expected_col)

    def test_get_column_dropped_column(
        self, dropped_cols_view: DropColsDataview
    ) -> None:
        """Test that get_column raises error if a dropped column is requested."""
        with pytest.raises(KeyError):
            dropped_cols_view.get_column("int_column")

        # Check that the "dropped column" was in the underlying data
        assert "int_column" in cast(
            pd.DataFrame, dropped_cols_view._datasource.get_data()
        )

    def test_get_dtypes(
        self, columns_to_drop: List[str], dropped_cols_view: DropColsDataview
    ) -> None:
        """Test that get_dtypes works as expected."""
        dtypes = dropped_cols_view.get_dtypes()

        # Don't make assertions on actual dtypes as these may be platform dependent
        # Just want to check that dropped columns aren't present
        for i in columns_to_drop:
            assert i not in dtypes

    def test___len__(
        self, dataframe: pd.DataFrame, dropped_cols_view: DropColsDataview
    ) -> None:
        """Test that __len__ works as expected."""
        len_view = len(dropped_cols_view)

        # No rows are dropped so should be the same as the original dataframe
        # AND the same as the underlying dataframe.
        assert (
            len_view
            == 3
            == len(dataframe)
            == len(cast(pd.DataFrame, dropped_cols_view._datasource.get_data()))
        )


@unit_test
class TestDropColViewConfig:
    """Tests for DropColViewConfig."""

    @fixture
    def mock_datasource(self) -> Mock:
        """A mock datasource."""
        mock_datasource: Mock = create_autospec(CSVSource, instance=True)
        return mock_datasource

    @fixture
    def datasource(self) -> BaseSource:
        """A DataframeSource."""
        return create_datasource(classification=True)

    def test_constructor(self) -> None:
        """Test constructor method."""
        source = "some-dataset"
        drop_cols = ["some", "columns"]
        config = DropColViewConfig(drop_cols=drop_cols, source_dataset=source)

        assert hasattr(config, "source_dataset_name")
        assert config.source_dataset_name == source

    def test_build(self, mock_datasource: Mock) -> None:
        """Test build() method."""
        drop_cols = ["hello", "world"]
        config = DropColViewConfig(drop_cols, source_dataset="testA")
        mock_datasource.data_splitter = None
        view_datasource = config.build(mock_datasource)

        assert view_datasource._drop_cols == drop_cols

    def test_generate_schema(
        self, datasource: BaseSource, mocker: MockerFixture
    ) -> None:
        """Test generate_schema() method."""
        drop_cols = ["A", "M"]
        config = DropColViewConfig(drop_cols, source_dataset="test")
        view_datasource_schema = config.generate_schema(
            underlying_datasource=datasource, name="test"
        )
        assert isinstance(view_datasource_schema, BitfountSchema)
        assert view_datasource_schema.tables[0].name == "test"
        assert "A" not in view_datasource_schema.tables[0].features["continuous"]
        assert "B" in view_datasource_schema.tables[0].features["continuous"]
        assert "M" not in view_datasource_schema.tables[0].features["categorical"]
        assert "N" in view_datasource_schema.tables[0].features["categorical"]

    def test_generate_schema_force_stypes(
        self, datasource: BaseSource, mocker: MockerFixture
    ) -> None:
        """Test generate_schema() method with force_stypes."""
        drop_cols = ["A", "M"]
        force_stypes: MutableMapping[
            Union[_ForceStypeValue, _SemanticTypeValue], List[str]
        ] = {
            "continuous": ["A", "N", "C", "D"],
            "categorical": ["M", "B", "O", "P"],
        }
        config = DropColViewConfig(drop_cols, source_dataset="test")
        view_datasource_schema = config.generate_schema(
            underlying_datasource=datasource, name="test", force_stypes=force_stypes
        )
        assert isinstance(view_datasource_schema, BitfountSchema)
        assert view_datasource_schema.tables[0].name == "test"
        assert "A" not in view_datasource_schema.tables[0].features["continuous"]
        assert "N" in view_datasource_schema.tables[0].features["continuous"]
        assert "M" not in view_datasource_schema.tables[0].features["categorical"]
        assert "B" in view_datasource_schema.tables[0].features["categorical"]


@unit_test
class TestSQLViewConfig:
    """Tests for SQLViewConfig."""

    @fixture
    def mock_datasource(self) -> Mock:
        """A mock datasource."""
        mock_datasource: Mock = create_autospec(CSVSource, instance=True)
        return mock_datasource

    @fixture
    def datasource(self) -> BaseSource:
        """A DataframeSource fixture."""
        return create_datasource(classification=True)

    @fixture
    def con(self) -> Generator[sqlite3.Connection, None, None]:
        """Yields a connection to a test SQLite database.

        Closes the connection and deletes the database after the test.
        """
        db_name = f"{POD_NAME}.sqlite"
        if os.path.exists(db_name):
            os.remove(db_name)
        con = sqlite3.connect(db_name)
        yield con
        con.close()
        os.remove(db_name)

    def test_initialize(self) -> None:
        """Test initialize() method."""
        query = "SELECT * FROM "
        config = SQLViewConfig(query=query, source_dataset="test")
        config.initialize(POD_NAME)
        assert hasattr(config, "pod_name")
        assert config.pod_name == POD_NAME

    @pytest.mark.skipif(
        condition=platform.system() == "Windows",
        reason=(
            "Only works intermittently on Windows. "
            "Connection to database not always closed properly,"
            "leading to PermissionError."
        ),
    )
    def test_build(self, con: sqlite3.Connection, mock_datasource: Mock) -> None:
        """Test build() method."""
        query = "SELECT * FROM "
        config = SQLViewConfig(query=query, source_dataset="test")
        config.initialize(POD_NAME)
        mock_datasource.data_splitter = None
        view_datasource = config.build(underlying_datasource=mock_datasource)
        assert view_datasource.query == query

    @pytest.mark.skipif(
        condition=platform.system() == "Windows",
        reason=(
            "Only works intermittently on Windows. "
            "Connection to database not always closed properly,"
            "leading to PermissionError."
        ),
    )
    def test_generate_schema(
        self,
        datasource: BaseSource,
    ) -> None:
        """Test generate_schema() method."""
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")
        con = sqlite3.connect(f"{POD_NAME}.sqlite")
        cur = con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{POD_NAME}" ('rowID' INTEGER PRIMARY KEY)"""  # nosec # noqa: B950
        )
        df = cast(pd.DataFrame, datasource.get_data())
        for col in df.columns:
            cur.execute(
                f"ALTER TABLE '{POD_NAME}' ADD COLUMN '{col}' {_sql_type_name(df[col])}"  # noqa: B950
            )
        df.to_sql(POD_NAME, con=con, if_exists="append", index=False)
        query = f"SELECT A, B, M, N, TARGET FROM {POD_NAME}"
        config = SQLViewConfig(query, source_dataset="test")
        config.initialize(POD_NAME)
        view_datasource_schema = config.generate_schema(
            underlying_datasource=datasource, name="test"
        )
        assert isinstance(view_datasource_schema, BitfountSchema)
        assert view_datasource_schema.tables[0].name == "test"
        assert "A" in view_datasource_schema.tables[0].features["continuous"]
        assert "B" in view_datasource_schema.tables[0].features["continuous"]
        assert "M" in view_datasource_schema.tables[0].features["continuous"]
        assert "N" in view_datasource_schema.tables[0].features["continuous"]
        assert "TARGET" in view_datasource_schema.tables[0].features["continuous"]
        assert "C" not in view_datasource_schema.tables[0].features["continuous"]
        os.remove(f"{POD_NAME}.sqlite")

    @pytest.mark.skipif(
        condition=platform.system() == "Windows",
        reason=(
            "Only works intermittently on Windows. "
            "Connection to database not always closed properly,"
            "leading to PermissionError."
        ),
    )
    def test_generate_schema_force_stypes(
        self, datasource: BaseSource, mocker: MockerFixture
    ) -> None:
        """Test generate_schema() method with force_stypes."""
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")
        con = sqlite3.connect(f"{POD_NAME}.sqlite")
        cur = con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{POD_NAME}" ('rowID' INTEGER PRIMARY KEY)"""  # nosec # noqa: B950
        )
        df = cast(pd.DataFrame, datasource.get_data())
        for col in df.columns:
            cur.execute(
                f"ALTER TABLE '{POD_NAME}' ADD COLUMN '{col}' {_sql_type_name(df[col])}"  # noqa: B950
            )
        df.to_sql(POD_NAME, con=con, if_exists="append", index=False)
        query = f"SELECT A, B, M, N, TARGET FROM {POD_NAME}"
        config = SQLViewConfig(query, source_dataset="test")
        config.initialize(POD_NAME)
        force_stypes: MutableMapping[
            Union[_ForceStypeValue, _SemanticTypeValue], List[str]
        ] = {
            "continuous": ["A", "N", "C", "D"],
            "categorical": ["M", "B", "O", "P", "TARGET"],
        }
        view_datasource_schema = config.generate_schema(
            underlying_datasource=datasource, name="test", force_stypes=force_stypes
        )
        assert isinstance(view_datasource_schema, BitfountSchema)
        assert view_datasource_schema.tables[0].name == "test"
        assert "A" in view_datasource_schema.tables[0].features["continuous"]
        assert "B" in view_datasource_schema.tables[0].features["categorical"]
        assert "M" in view_datasource_schema.tables[0].features["categorical"]
        assert "N" in view_datasource_schema.tables[0].features["continuous"]
        assert "TARGET" in view_datasource_schema.tables[0].features["categorical"]
        assert "C" not in view_datasource_schema.tables[0].features["continuous"]
        os.remove(f"{POD_NAME}.sqlite")

    @pytest.mark.skipif(
        condition=platform.system() == "Windows",
        reason=(
            "Only works intermittently on Windows. "
            "Connection to database not always closed properly,"
            "leading to PermissionError."
        ),
    )
    def test_generate_schema_force_stypes_image_prefix(
        self, datasource: BaseSource, mocker: MockerFixture
    ) -> None:
        """Test generate_schema() method with force_stypes."""
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")
        con = sqlite3.connect(f"{POD_NAME}.sqlite")
        cur = con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{POD_NAME}" ('rowID' INTEGER PRIMARY KEY)"""  # nosec # noqa: B950
        )
        df = cast(pd.DataFrame, datasource.get_data())
        for col in df.columns:
            cur.execute(
                f"ALTER TABLE '{POD_NAME}' ADD COLUMN '{col}' {_sql_type_name(df[col])}"  # noqa: B950
            )
        df.to_sql(POD_NAME, con=con, if_exists="append", index=False)
        query = f"SELECT A, B, M, N, TARGET FROM {POD_NAME}"
        config = SQLViewConfig(query, source_dataset="test")
        config.initialize(POD_NAME)
        force_stypes: MutableMapping[
            Union[_ForceStypeValue, _SemanticTypeValue], List[str]
        ] = {
            "continuous": ["N", "C", "D"],
            "categorical": ["M", "B", "O", "P", "TARGET"],
            "image_prefix": ["A"],
        }
        mock_get_column = mocker.patch(
            "bitfount.data.datasources.views.SQLDataView.get_column"
        )
        mock_get_column.return_value = []
        view_datasource_schema = config.generate_schema(
            underlying_datasource=datasource, name="test", force_stypes=force_stypes
        )
        assert isinstance(view_datasource_schema, BitfountSchema)
        assert view_datasource_schema.tables[0].name == "test"
        assert "A" in view_datasource_schema.tables[0].features["image"]
        assert "B" in view_datasource_schema.tables[0].features["categorical"]
        assert "M" in view_datasource_schema.tables[0].features["categorical"]
        assert "N" in view_datasource_schema.tables[0].features["continuous"]
        assert "TARGET" in view_datasource_schema.tables[0].features["categorical"]
        assert "C" not in view_datasource_schema.tables[0].features["continuous"]
        os.remove(f"{POD_NAME}.sqlite")

    @pytest.mark.skipif(
        condition=platform.system() == "Windows",
        reason=(
            "Only works intermittently on Windows. "
            "Connection to database not always closed properly,"
            "leading to PermissionError."
        ),
    )
    def test_generate_schema_force_stypes_image_prefix_img_col(
        self, datasource: BaseSource, mocker: MockerFixture
    ) -> None:
        """Test generate_schema() method with force_stypes."""
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")
        con = sqlite3.connect(f"{POD_NAME}.sqlite")
        cur = con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{POD_NAME}" ('rowID' INTEGER PRIMARY KEY)"""  # nosec # noqa: B950
        )
        df = cast(pd.DataFrame, datasource.get_data())
        for col in df.columns:
            cur.execute(
                f"ALTER TABLE '{POD_NAME}' ADD COLUMN '{col}' {_sql_type_name(df[col])}"  # noqa: B950
            )
        df.to_sql(POD_NAME, con=con, if_exists="append", index=False)
        query = f"SELECT A, B, M, N, TARGET FROM {POD_NAME}"
        config = SQLViewConfig(query, source_dataset="test")
        config.initialize(POD_NAME)
        force_stypes: MutableMapping[
            Union[_ForceStypeValue, _SemanticTypeValue], List[str]
        ] = {
            "continuous": ["N", "C", "D"],
            "categorical": ["M", "O", "P", "TARGET"],
            "image_prefix": ["A"],
            "image": ["B"],
        }
        mock_get_column = mocker.patch(
            "bitfount.data.datasources.views.SQLDataView.get_column"
        )
        mock_get_column.return_value = []
        view_datasource_schema = config.generate_schema(
            underlying_datasource=datasource, name="test", force_stypes=force_stypes
        )
        assert isinstance(view_datasource_schema, BitfountSchema)
        assert view_datasource_schema.tables[0].name == "test"
        assert "A" in view_datasource_schema.tables[0].features["image"]
        assert "B" in view_datasource_schema.tables[0].features["image"]
        assert "M" in view_datasource_schema.tables[0].features["categorical"]
        assert "N" in view_datasource_schema.tables[0].features["continuous"]
        assert "TARGET" in view_datasource_schema.tables[0].features["categorical"]
        assert "C" not in view_datasource_schema.tables[0].features["continuous"]
        os.remove(f"{POD_NAME}.sqlite")

    @pytest.mark.skipif(
        condition=platform.system() == "Windows",
        reason=(
            "Only works intermittently on Windows. "
            "Connection to database not always closed properly,"
            "leading to PermissionError."
        ),
    )
    def test_generate_schema_force_stypes_image_prefix_img_cols(
        self, datasource: BaseSource, mocker: MockerFixture
    ) -> None:
        """Test generate_schema() method with force_stypes."""
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")
        con = sqlite3.connect(f"{POD_NAME}.sqlite")
        cur = con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{POD_NAME}" ('rowID' INTEGER PRIMARY KEY)"""  # nosec # noqa: B950
        )
        df = cast(pd.DataFrame, datasource.get_data())
        for col in df.columns:
            cur.execute(
                f"ALTER TABLE '{POD_NAME}' ADD COLUMN '{col}' {_sql_type_name(df[col])}"  # noqa: B950
            )
        df.to_sql(POD_NAME, con=con, if_exists="append", index=False)
        query = f"SELECT A, B, M, N, TARGET FROM {POD_NAME}"
        config = SQLViewConfig(query, source_dataset="test")
        config.initialize(POD_NAME)
        force_stypes: MutableMapping[
            Union[_ForceStypeValue, _SemanticTypeValue], List[str]
        ] = {
            "continuous": ["N", "C", "D"],
            "categorical": ["M", "O", "P", "TARGET"],
            "image": ["B"],
            "image_prefix": ["A"],
        }
        mock_get_column = mocker.patch(
            "bitfount.data.datasources.views.SQLDataView.get_column"
        )
        mock_get_column.return_value = []
        view_datasource_schema = config.generate_schema(
            underlying_datasource=datasource, name="test", force_stypes=force_stypes
        )
        assert isinstance(view_datasource_schema, BitfountSchema)
        assert view_datasource_schema.tables[0].name == "test"
        assert "A" in view_datasource_schema.tables[0].features["image"]
        assert "B" in view_datasource_schema.tables[0].features["image"]
        assert "M" in view_datasource_schema.tables[0].features["categorical"]
        assert "N" in view_datasource_schema.tables[0].features["continuous"]
        assert "TARGET" in view_datasource_schema.tables[0].features["categorical"]
        assert "C" not in view_datasource_schema.tables[0].features["continuous"]
        os.remove(f"{POD_NAME}.sqlite")

    @pytest.mark.skipif(
        condition=platform.system() == "Windows",
        reason=(
            "Only works intermittently on Windows. "
            "Connection to database not always closed properly,"
            "leading to PermissionError."
        ),
    )
    def test_generate_schema_force_stypes_image(
        self, datasource: BaseSource, mocker: MockerFixture
    ) -> None:
        """Test generate_schema() method with force_stypes."""
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")
        con = sqlite3.connect(f"{POD_NAME}.sqlite")
        cur = con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{POD_NAME}" ('rowID' INTEGER PRIMARY KEY)"""  # nosec # noqa: B950
        )
        df = cast(pd.DataFrame, datasource.get_data())
        for col in df.columns:
            cur.execute(
                f"ALTER TABLE '{POD_NAME}' ADD COLUMN '{col}' {_sql_type_name(df[col])}"  # noqa: B950
            )
        df.to_sql(POD_NAME, con=con, if_exists="append", index=False)
        query = f"SELECT A, B, M, N, TARGET FROM {POD_NAME}"
        config = SQLViewConfig(query, source_dataset="test")
        config.initialize(POD_NAME)
        force_stypes: MutableMapping[
            Union[_ForceStypeValue, _SemanticTypeValue], List[str]
        ] = {
            "continuous": ["A", "N", "C", "D"],
            "categorical": ["M", "O", "P", "TARGET"],
            "image": ["B"],
        }
        mock_get_column = mocker.patch(
            "bitfount.data.datasources.views.SQLDataView.get_column"
        )
        mock_get_column.return_value = []
        view_datasource_schema = config.generate_schema(
            underlying_datasource=datasource, name="test", force_stypes=force_stypes
        )
        assert isinstance(view_datasource_schema, BitfountSchema)
        assert view_datasource_schema.tables[0].name == "test"
        assert "A" in view_datasource_schema.tables[0].features["continuous"]
        assert "B" in view_datasource_schema.tables[0].features["image"]
        assert "M" in view_datasource_schema.tables[0].features["categorical"]
        assert "N" in view_datasource_schema.tables[0].features["continuous"]
        assert "TARGET" in view_datasource_schema.tables[0].features["categorical"]
        assert "C" not in view_datasource_schema.tables[0].features["continuous"]
        os.remove(f"{POD_NAME}.sqlite")


@pytest.mark.skipif(
    condition=platform.system() == "Windows",
    reason=(
        "Only works intermittently on Windows. "
        "Connection to database not always closed properly,"
        "leading to PermissionError."
    ),
)
@unit_test
class TestSQLDataView:
    """Class for testing SQLDataViews."""

    def dicom_files_2d(self, tmp_path: Path, filename: str = "dicom_file") -> None:
        """Generates five 2d dicom files for testing."""
        for i in range(5):
            filepath = tmp_path / f"{filename}_{i}.dcm"
            pixel_arr = np.random.randint(0, 255, (100, 100))
            file_meta = FileMetaDataset()
            ds = FileDataset(filepath, {}, file_meta=file_meta, preamble=b"\0" * 128)
            ds.PatientName = f"Patient {i}"
            ds.PatientID = f"ID {i}"
            ds.StudyDate = f"{datetime.date.today()}"
            ds.StudyTime = f"{i}"
            ds.StudyDescription = "Test"
            ds.PixelData = pixel_arr.tobytes()
            ds.NumberOfFrames = "1"
            ds.BitsAllocated = 8
            ds.SamplesPerPixel = 1
            ds.Rows = 100
            ds.Columns = 100
            ds.PhotometricInterpretation = "RGB"
            ds.PixelRepresentation = 0
            ds.BitsStored = 8
            ds.file_meta = FileMetaDataset()
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian  # type: ignore[attr-defined] # Reason: pydicom has that attr and we only use it for testing. # noqa: B950
            ds.is_little_endian = False
            ds.is_implicit_VR = False
            ds.save_as(filepath)

    @fixture
    def mock_datasource(self) -> Mock:
        """A mock datasource."""
        mock_datasource: Mock = create_autospec(CSVSource, instance=True)
        return mock_datasource

    @fixture
    def datasource(self) -> BaseSource:
        """A DataframeSource."""
        return create_datasource(classification=True)

    @fixture
    def dicom_2dsource(self, tmp_path: Path) -> DICOMSource:
        """CSVSource."""
        self.dicom_files_2d(tmp_path)
        datasource = DICOMSource(path=tmp_path, output_path=tmp_path)
        return datasource

    @fixture
    def query_dicom(self) -> str:
        """Query for the view from a dicom datasource."""
        return f'SELECT "Pixel Data 0" FROM "{POD_NAME_DICOM}"'

    @fixture
    def sql_view_file_iterable(
        self, mocker: MockerFixture, query_dicom: str, dicom_2dsource: DICOMSource
    ) -> SQLDataView:
        """The view datasource with SQL views."""
        # Tests pass locally on OSX in both instances but
        # sometimes fail on the CI, hence the `try...except`.
        # What makes it even weirder is that some tests pass
        # and some tests fail when they are using excatly the same fixture.
        try:
            sql_view = SQLDataView(
                dicom_2dsource,
                query_dicom,
                POD_NAME_DICOM,
                source_dataset_name=POD_NAME_DICOM,
            )
        except ValueError:
            try:
                query = f'SELECT "Pixel Data 0" FROM {POD_NAME_DICOM}'
                sql_view = SQLDataView(
                    dicom_2dsource,
                    query,
                    POD_NAME_DICOM,
                    source_dataset_name=POD_NAME_DICOM,
                )
            except ValueError:
                with mocker.patch(
                    "bitfount.data.datasources.views.SQLDataView._get_filenames"
                ):
                    sql_view = SQLDataView(
                        dicom_2dsource,
                        query_dicom,
                        POD_NAME_DICOM,
                        source_dataset_name=POD_NAME_DICOM,
                    )
        return sql_view

    @fixture
    def pod_conn_file_iterable(self, dicom_2dsource: BaseSource) -> None:
        """Fixture for setting up pod db connection."""
        if os.path.exists(f"{POD_NAME_DICOM}.sqlite"):
            os.remove(f"{POD_NAME_DICOM}.sqlite")
        con = sqlite3.connect(f"{POD_NAME_DICOM}.sqlite")
        cur = con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{POD_NAME_DICOM}" ("rowID" INTEGER PRIMARY KEY)"""  # nosec # noqa: B950
        )
        df = cast(pd.DataFrame, dicom_2dsource.get_data())
        for col in df.columns:
            cur.execute(
                f"""ALTER TABLE "{POD_NAME_DICOM}" ADD COLUMN "{col}" {_sql_type_name(df[col])}"""  # noqa: B950
            )
        df.to_sql(POD_NAME_DICOM, con=con, if_exists="append", index=False)

    @fixture
    def query(self) -> str:
        """Query for the view."""
        return f"SELECT A, B, M, N, TARGET FROM {POD_NAME}"

    @fixture
    def sql_view(self, query: str, datasource: BaseSource) -> SQLDataView:
        """The view datasource with sql query."""
        return SQLDataView(datasource, query, POD_NAME, source_dataset_name=POD_NAME)

    @fixture
    def pod_conn(self, datasource: BaseSource) -> None:
        """Fixture for setting up pod db connection."""
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")
        con = sqlite3.connect(f"{POD_NAME}.sqlite")
        cur = con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{POD_NAME}" ("rowID" INTEGER PRIMARY KEY)"""  # nosec # noqa: B950
        )
        df = cast(pd.DataFrame, datasource.get_data())
        for col in df.columns:
            cur.execute(
                f"""ALTER TABLE "{POD_NAME}" ADD COLUMN "{col}" {_sql_type_name(df[col])}"""  # noqa: B950
            )
        df.to_sql(POD_NAME, con=con, if_exists="append", index=False)

    def test_get_data(
        self, sql_view: SQLDataView, pod_conn: sqlite3.Connection
    ) -> None:
        """Test that get_data returns a dataframe with sql query output."""
        data = sql_view.get_data()
        assert data.shape == (4000, 5)
        assert set(data.columns) == set(["A", "B", "M", "N", "TARGET"])
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")

    def test_get_values(
        self, sql_view: SQLDataView, pod_conn: sqlite3.Connection
    ) -> None:
        """Test that get_values works as expected."""
        data = sql_view.get_values(["N", "M"])
        assert set(data.keys()) == set(["N", "M"])
        assert set(data["N"]) == set([0, 1])
        assert set(data["M"]) == set([0, 1])
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")

    def test_get_column(
        self, sql_view: SQLDataView, pod_conn: sqlite3.Connection
    ) -> None:
        """Test that get_values works as expected."""
        data = sql_view.get_column("N")
        assert isinstance(data, pd.Series)
        assert len(data) == 4000
        assert data.name == "N"
        assert set(data.unique()) == set([0, 1])
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")

    def test_get_dtypes(
        self, query: str, sql_view: SQLDataView, pod_conn: sqlite3.Connection
    ) -> None:
        """Test that get_dtypes works as expected."""
        dtypes = sql_view.get_dtypes()
        # Don't make assertions on actual dtypes as these may be platform dependent
        # Just want to check that columns returned are found in the query
        for k in dtypes.keys():
            assert k in query
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")

    def test_get_tables(
        self, sql_view: SQLDataView, pod_conn: sqlite3.Connection
    ) -> None:
        """Test get_tables works as expected."""
        tables = sql_view.get_tables()
        assert tables == ["testpod"]
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")

    def test___len__(
        self,
        datasource: BaseSource,
        sql_view: SQLDataView,
        pod_conn: sqlite3.Connection,
    ) -> None:
        """Test that __len__ works as expected."""
        len_view = len(sql_view)

        # No rows are dropped so should be the same as the original dataframe
        # AND the same as the underlying dataframe.
        assert isinstance(sql_view._datasource.get_data(), pd.DataFrame)
        assert isinstance(datasource.get_data(), pd.DataFrame)
        assert (
            len_view
            == 4000
            == len(cast(pd.DataFrame, datasource.get_data()))
            == len(cast(pd.DataFrame, sql_view._datasource.get_data()))
        )
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")

    def test___len__filter_query(
        self, datasource: BaseSource, pod_conn: sqlite3.Connection
    ) -> None:
        """Test that __len__ works as expected."""
        query = f"SELECT M FROM {POD_NAME} where M==0"
        sql_view = SQLDataView(datasource, query, POD_NAME, POD_NAME)
        len_view = len(sql_view)
        df = cast(pd.DataFrame, datasource.get_data())
        assert len_view == df["M"].value_counts()[False] == len(sql_view.get_data())
        if os.path.exists(f"{POD_NAME}.sqlite"):
            os.remove(f"{POD_NAME}.sqlite")

    def test_get_data_file_iterable(
        self,
        sql_view_file_iterable: SQLDataView,
        pod_conn_file_iterable: sqlite3.Connection,
    ) -> None:
        """Test that get_data returns a dataframe with sql query output."""
        data = sql_view_file_iterable.get_data()
        assert data.shape == (5, 1)
        assert set(data.columns) == set(["Pixel Data 0"])
        if os.path.exists(f"{POD_NAME_DICOM}.sqlite"):
            os.remove(f"{POD_NAME_DICOM}.sqlite")

    def test_get_values_file_iterable(
        self,
        sql_view_file_iterable: SQLDataView,
        pod_conn_file_iterable: sqlite3.Connection,
    ) -> None:
        """Test that get_values works as expected."""
        data = sql_view_file_iterable.get_values(["Pixel Data 0"])
        assert set(data.keys()) == set(["Pixel Data 0"])
        assert len(data["Pixel Data 0"]) == 5  # type: ignore[arg-type] # reason: testing purposes # noqa: B950
        if os.path.exists(f"{POD_NAME_DICOM}.sqlite"):
            os.remove(f"{POD_NAME_DICOM}.sqlite")

    def test_get_column_file_iterable(
        self,
        sql_view_file_iterable: SQLDataView,
        pod_conn_file_iterable: sqlite3.Connection,
    ) -> None:
        """Test that get_values works as expected."""
        data = sql_view_file_iterable.get_column("Pixel Data 0")
        assert isinstance(data, pd.Series)
        assert len(data) == 5
        assert data.name == "Pixel Data 0"
        if os.path.exists(f"{POD_NAME_DICOM}.sqlite"):
            os.remove(f"{POD_NAME_DICOM}.sqlite")

    def test_get_tables_file_iterable(
        self,
        sql_view_file_iterable: SQLDataView,
        pod_conn_file_iterable: sqlite3.Connection,
    ) -> None:
        """Test get_tables works as expected."""
        tables = sql_view_file_iterable.get_tables()
        assert tables == [POD_NAME_DICOM]
        if os.path.exists(f"{POD_NAME_DICOM}.sqlite"):
            os.remove(f"{POD_NAME_DICOM}.sqlite")

    def test___len___file_iterable(
        self,
        dicom_2dsource: BaseSource,
        sql_view_file_iterable: SQLDataView,
        pod_conn_file_iterable: sqlite3.Connection,
    ) -> None:
        """Test that __len__ works as expected."""
        len_view = len(sql_view_file_iterable)

        # No rows are dropped so should be the same as the original dataframe
        # AND the same as the underlying dataframe.
        assert isinstance(sql_view_file_iterable._datasource.get_data(), pd.DataFrame)
        assert isinstance(dicom_2dsource.get_data(), pd.DataFrame)
        assert (
            len_view
            == 5
            == len(cast(pd.DataFrame, dicom_2dsource.get_data()))
            == len(cast(pd.DataFrame, sql_view_file_iterable._datasource.get_data()))
        )
        if os.path.exists(f"{POD_NAME_DICOM}.sqlite"):
            os.remove(f"{POD_NAME_DICOM}.sqlite")

    def test___len__filter_query_file_iterable(
        self, dicom_2dsource: BaseSource, pod_conn_file_iterable: sqlite3.Connection
    ) -> None:
        """Test that __len__ works as expected."""
        query = f'SELECT "Pixel Data 0" FROM {POD_NAME_DICOM}'
        sql_view = SQLDataView(dicom_2dsource, query, POD_NAME_DICOM, POD_NAME_DICOM)
        len_view = len(sql_view)
        assert len_view == 5
        if os.path.exists(f"{POD_NAME_DICOM}.sqlite"):
            os.remove(f"{POD_NAME_DICOM}.sqlite")

    def test_yield_data_2d(
        self, dicom_2dsource: DICOMSource, pod_conn_file_iterable: sqlite3.Connection
    ) -> None:
        """Test yield_data for view from DICOMSource."""
        dicom_2dsource.partition_size = 2
        query = f'SELECT "Pixel Data 0" FROM {POD_NAME_DICOM}'
        sql_view = SQLDataView(dicom_2dsource, query, POD_NAME_DICOM, POD_NAME_DICOM)
        # There are 5 rows in the test data, so we should get 3 partitions
        for i, partition in enumerate(sql_view.yield_data()):
            # Asserting that the partition is a dataframe
            assert isinstance(partition, pd.DataFrame)
            if i == 2:  # Last partition
                # Asserting that the last partition has 1 row
                assert len(partition) == 1
            else:
                # Asserting that the other partitions have 2 rows
                assert len(partition) == 2
        if os.path.exists(f"{POD_NAME_DICOM}.sqlite"):
            os.remove(f"{POD_NAME_DICOM}.sqlite")

    def test_yield_data_error(self, sql_view: SQLDataView) -> None:
        """Test yield_data for view non-iterable raises error."""
        with pytest.raises(ValueError):
            for _, _ in enumerate(sql_view.yield_data()):
                pass

    @pytest.mark.skip(reason="Flaky test, to investigate.")
    def test__get_filenames_raises_error(
        self, mocker: MockerFixture, sql_view_file_iterable: SQLDataView
    ) -> None:
        """Tests that _get_filenames raises error when query fails."""
        mocker.patch.object(pd, "read_sql_query", side_effect=ValueError)
        with pytest.raises(SQLViewError):
            sql_view_file_iterable._get_filenames()
