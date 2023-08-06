import json
import shutil
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path
from typing import Any

from loguru import logger
from tinydb import Query, TinyDB

from frogbase.captions import Captions
from frogbase.config import FrogBaseConfig
from frogbase.media import Media, MediaManager
from frogbase.models import ModelManager


class FrogBase:
    """
    Core entry point to manage a multitude of media sources, speech-to-text
    models, language models, and ann indices.
    FrogBase operates primarily on Media objects that are grouped into separate
    collections (libraries) that map to a directory within the data directory.
    NOTE: Libraries are physical separations of data which means that copies
    of the same media can exist in different libraries. For logical separation,
    use tags on media objects.
    """

    def __init__(
        self,
        datadir: str = "./frogverse",
        library: str = "main",
        persist: bool = True,
        verbose: bool = False,
        dev: bool = False,
    ) -> None:
        """Initialize a 🐸 FrogBase instance.

        Args:
            datadir: Houses all data for a FrogBase instance. Defaults to "./frogverse".
            library: The name of the library to use. Defaults to "main".
            persist: Whether to persist the data to disk. Defaults to True.
                Warning: If set to False, all data is stored in a temporary directory
                that is deleted when the instance is destroyed. Use this only if
                you're playing around or you maintain external states to keep track
                of the data.
            verbose: Whether to print verbose logs.
            dev: Flag to control development mode. This is useful for
                debugging and testing.
        """

        # Config specific to devmode & production mode.
        self._version = "dev" if dev else version("frogbase")
        self._verbose = True if dev else verbose
        self._dev = dev

        # Create a logger that streams to stdout and set verbosity level.
        self._logger = logger
        self._logger.remove()
        log_level = "DEBUG" if self._dev else "INFO" if self._verbose else "WARNING"
        # If dev mode is not set, use a friendly log format.
        if self._dev:
            self._logger.add(
                sys.stdout,
                level=log_level,
                format="[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>] | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - 🐸 <level>{message}</level>",
            )
        else:
            self._logger.add(
                sys.stdout,
                level=log_level,
                format="<level>[{level}] </level>🐸 <level>{message}</level>",
            )

        # Print a log message about initializing the FrogBase instance & version.
        self._logger.info(f"Initializing FrogBase instance: <version: {self._version}>")

        # Add warning that the version is alpha and may be unstable.
        if "dev" in self._version or "a" in self._version:
            self._logger.warning(
                "Hi! You're using an alpha version of FrogBase. "
                "This will be unstable and is likely to break. "
                "Please flag any issues at https://github.com/hayabhay/frogbase/issues"
            )

        # If persist is set to True, create a directory to store all the data.
        # Otherwise, store all the data in a temporary directory that is
        # deleted when the instance is destroyed.
        self._datadir = Path(datadir)
        if not persist:
            # NOTE: For devs: It is important to save this temp directory
            # path in an object attribute. Otherwise, the directory is deleted when
            # the reference is lost.
            self._tmpdir = tempfile.TemporaryDirectory()
            self._datadir = Path(self._tmpdir.name) / self._datadir.name

        # Create the datadir if it doesn't exist.
        self._datadir.mkdir(parents=True, exist_ok=True)

        # Next, set the library to use for the FrogBase instance and create
        # the library directory if it doesn't exist.
        self._default_library = library

        # NOTE: The library setter initializes a "session" of sorts. Specifically,
        # 1. It sets the library name & path along with creating the directory.
        # 2. It initializes tinydb & purges/clears/recover db as needed.
        # 3. It updates table references & managers for the FrogBase instance.
        # In addition, a fair number of variables are set up in the library setter.
        self.library = self._default_library

        self._media_buffer = []
        self._index = None

        # NOTE: Do not add any code after the library setter unless they're
        # related to the library setter.

    def __repr__(self) -> str:
        return f"<FrogBase: {self._libdir}>"

    def __str__(self) -> str:
        return self.__repr__()

    # ------------------------ Library Management  --------------------------
    @property
    def library(self) -> str:
        """The name of the library to use."""
        return self._library

    @library.setter
    def library(self, library: str) -> None:
        """Set the library to use for the FrogBase instance."""
        self._logger.info(f"Setting up library: {library}")
        self._libdir = self._datadir / library
        self._libdir.mkdir(parents=True, exist_ok=True)
        self._library = library
        self._logger.info(f"Library path: {self._libdir}")

        # Next, initialize tinydb & purge/clear/recover db as needed.
        # Also, update managers for the FrogBase instance.
        self._initdb()

        # Once library is initialized, create a config object and initialize
        # all the necessary managers
        self.config = FrogBaseConfig(
            datadir=self._datadir,
            libdir=self._libdir,
            db=self._db,
            logger=self._logger,
            dev=self._dev,
            verbose=self._verbose,
            download_archive=self._libdir / "downloaded_media.txt",
        )
        # Initialize media manager.
        self.media = MediaManager(self.config)
        # Initialize model manager.
        self.models = ModelManager(self.config)

    # Function to burn a FrogBase library to the digital ground.
    def remove_library(self, name: str) -> None:
        """Remove a library from the FrogBase instance."""
        self._logger.info(f"Removing library: {name}")
        shutil.rmtree(self._datadir / name)
        # Check if the library being removed is the current library.
        # If so, set the library to the default library.
        if name == self._library:
            self.library = self._default_library

    # ---------------------------- TinyDB Init ------------------------------
    def _initdb(self) -> bool:
        """Initialize the tinydb instance for the FrogBase instance given
        the current library.
        """
        self._logger.info(f"Initializing TinyDB instance for library: {self._library}")
        # FrogBase saves all meta information with TinyDB in addition to
        # raw files on disk for simpler search & filter operations.
        dbname = "tinydb-dev.json" if self._dev else "tinydb.json"
        # Set the path to the tinydb json file.
        self._dbpath = self._libdir / dbname
        # Load the tinydb instance if it exists.
        self._db = TinyDB(self._dbpath) if self._dbpath.exists() else None
        self._logger.info(f"TinyDB path: {self._dbpath}")

        # First check if the tinydb instance exists and if it is compatible
        # with the current version of FrogBase. If not, delete the tinydb
        # json and re-create it.
        # NOTE: Right now any version change will re-create tinydb and purge
        # all existing data to ensure compatibility. Later, this can be updated
        # to only re-create the tinydb data if the minor version changes.
        # NOTE: Temporary hack to kill tinydb if it fails to load. Fix this later
        try:
            db_meta = self._db.get(Query().type == "meta") if self._db else None
        except Exception as e:
            self._logger.error(f"Failed to load tinydb instance. Error: {e}")
            self._db.close()
            self._dbpath.unlink()
            self._db = None

        if db_meta and db_meta["__version__"] < self._version:
            self._logger.info(f"Existing tinydb version: {db_meta['__version__']} is stale. Removing.")
            self._db.close()
            self._dbpath.unlink()
            self._db = None

        # Next, if the tinydb instance never existed or was deleted from being stale, create a new one.
        if not self._db:
            self._logger.info("TinyDB instance either doesn't exist or is stale. Creating a new one.")
            self._db = TinyDB(self._dbpath)
            self._db.insert({"type": "meta", "__version__": self._version})

            # Next, attempt to recover the media files
            self._logger.info("Attempting to recover media metadata.")
            # Look for all metadata files in the .bkup directory and load them.
            media_dicts = []
            for infopath in self._libdir.glob("**/.bkup/*.media.fb.json"):
                self._logger.info(f"Recovering media metadata from {infopath}")
                with open(infopath) as f:
                    media_dicts.append(json.load(f))
            # Insert the recovered media metadata into the db.
            self._db.table(Media.__name__).insert_multiple(media_dicts)

            # Next, attempt to recover the captions files
            self._logger.info("Attempting to recovering caption metadata")
            # Look for all metadata files in the .bkup directory and load them.
            caption_dicts = []
            for infopath in self._libdir.glob("**/.bkup/*.captions.fb.json"):
                self._logger.info(f"Recovering caption metadata from {infopath}")
                with open(infopath) as f:
                    caption_dicts.append(json.load(f))
            # Insert the recovered caption metadata into the db.
            self._db.table(Captions.__name__).insert_multiple(caption_dicts)

    # ------------------------ Primary Interface ----------------------------
    def add(self, sources: str | list[str], **opts: dict[str, Any]) -> "FrogBase":
        """Adds one or more media sources to the FrogBase library.
        These media sources can be urls or file/directory paths on disk.

        Args:
            sources: One or more media sources to add. Allowed sources are urls or filepaths on disk.
               Single source can be passed as a string instead of a list as a convenience.
            **opts: Source type specific options. Check the source type specific methods for more info.
        """
        if not isinstance(sources, list):
            sources = [sources]

        self._logger.info(f"Adding media {len(sources)} sources to library: {self._library}")
        self._media_buffer = self.media.add(sources, **opts)
        self._logger.info(f"Added {len(self._media_buffer)} new media to the library.")

        return self

    def transcribe(
        self,
        media: None | Media | list[Media] = None,
        transcriber: str | None = None,
        model: str | None = None,
        keep_model_in_memory: bool = False,
        ignore_captioned: bool = False,
        **params: Any,
    ) -> "FrogBase":
        """Transcribes the media sources added to the FrogBase instance."""
        # If running without arguments, assume it is running in chain mode.
        # If nothing is in the media buffer, use all media in the library.
        for media_obj in self._media_buffer:
            self._logger.info(f"Transcribing media: {media_obj.title}")

        if not media:
            if self._media_buffer:
                self._logger.info(f"Transcribing {len(self._media_buffer)} media in the batch.")
                media = self._media_buffer
            else:
                self._logger.info("Transcribing all the media in the library.")
                media = self.media.all()

        if ignore_captioned:
            media = [media_obj for media_obj in media if not media_obj.has_captions()]
            self._logger.info(f"Ignoring captioned media. {len(media)} media remaining.")

        self.models.transcribe(media, transcriber, model, keep_model_in_memory, **params)

        return self

    def embed(
        self,
        media: None | Media | list[Media] = None,
        embedder: str | None = None,
        model: str | None = None,
        keep_model_in_memory: bool = False,
        overwrite: bool = False,
        **params: dict[str, Any],
    ) -> "FrogBase":
        """Embed one or more media with a specified vectorization engine and parameters."""
        # If running without arguments, assume it is running in chain mode.
        # If nothing is in the media buffer, use all media in the library.
        if not media:
            if self._media_buffer:
                self._logger.info(f"Vectorizing {len(self._media_buffer)} media in the batch.")
                media = self._media_buffer
            else:
                self._logger.info("Vectorizing all the media in the library.")
                media = self.media.all()

        self.models.embed(media, embedder, model, keep_model_in_memory, overwrite, **params)

        return self

    def index(
        self,
        # media: None | Media | list[Media] = None,
        indexer: str | None = None,
        embedding_source: str | None = None,
        **params: dict[str, Any],
    ) -> dict[str, Any]:
        """Builds a search index from the embedded media."""
        # TODO: Fix this
        # # If running without arguments, assume it is running in chain mode.
        # # If nothing is in the media buffer, use all media in the library.
        # if not media:
        #     if self._media_buffer:
        #         self._logger.info(f"Building index for {len(self._media_buffer)} media in the batch.")
        #         media = self._media_buffer
        #     else:
        #         self._logger.info("Building index for all the media in the library.")
        #         media = self.media.all()

        self._index = self.models.index(indexer, embedding_source, **params)
        # self._index = self.models.index(media, indexer, embedding_source, **params)

        return self._index

    # NOTE: This is currently a hacky function just for the Streamlit UI
    # TODO: This needs to be cleaned up
    def search(
        self,
        query: str,
        k: int = 10,
        index: None | dict[str, Any] = None,
    ) -> list[dict[str, Any]]:
        """Searches the index for the query string."""
        # TODO: Fix this
        if not index:
            if not self._index:
                index = self.index()
            else:
                index = self._index
        if not index:
            raise ValueError("No index found. Please load an index first.")

        # First encode the query
        query = self._index["encoder"].encode(query)
        # Then search the index
        entity_ids, distances = self._index["index"].knn_query(query, k=k)

        results = []
        for entity_id, distance in zip(entity_ids[0], distances[0]):
            # Get the label for the segment
            label = self._index["meta"][entity_id]
            media_id, caption_id, segment_id, start_time = label.split("::")
            media_obj = self.media.get(media_id)
            captions_obj = media_obj.captions.get(caption_id)
            captions = list(captions_obj.load())
            results.append({"media": media_obj, "segment": captions[int(segment_id)], "score": float(1 - distance)})

        return results

    def demo(self) -> None:
        """Runs a demo version of the entire FrogBase pipeline.
        1. Downloads a youtube video.
        2. Transcribes the video using a speech-to-text model.
        3. Embeds transcript segments using sentence-transformers.
        4. Builds a search index using hnswlib.
        """
        sources = [
            "https://www.tiktok.com/@hayabhay/video/7156262943372381486",
            "https://www.youtube.com/watch?v=HBxn56l9WcU",
        ]
        self.add(sources, audio_only=False).transcribe(ignore_captioned=False).embed(overwrite=False).index()
